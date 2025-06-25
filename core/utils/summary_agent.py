from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

# Configure logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load OpenAI API key
try:
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    logger.info("OpenAI API configured successfully.")
except Exception as e:
    logger.error(f"Failed to configure OpenAI API: {e}")
    raise

# LangGraph shared state schema
class SummaryState(TypedDict, total=False):
    chunks: List[str]
    summaries: List[str]
    narrative_script: str

# Step 1: Summarize PDF chunks
def summarize_chunks(state: SummaryState) -> SummaryState:
    """Summarize each chunk of text using the OpenAI model."""
    try:
        summaries = []
        for chunk in state["chunks"]:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert assistant who summarizes content concisely and clearly for the targeted audience."},
                    {"role": "user", "content": f"Summarize this content:\n\n{chunk}"}
                ],
                max_tokens=150,
                temperature=0.7
            )
            summaries.append(response.choices[0].message.content)
        logger.info(f"Summarized {len(summaries)} chunks successfully.")
        return {"summaries": summaries}
    except Exception as e:
        logger.error(f"Error summarizing chunks: {e}")
        raise

# Step 2: Convert to narrative format
def generate_narrative(state: SummaryState) -> SummaryState:
    """Convert summarized chunks into a human-friendly narrative."""
    try:
        full_text = "\n".join(state["summaries"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert assistant that transforms summaries into an engaging, human-friendly narrative for non-expert readers. Use clear language, logical transitions, and avoid unnecessary jargon."},
                {"role": "user", "content": f"Create a cohesive narrative from these summaries:\n\n{full_text}"}
            ],
            max_tokens=500,
            temperature=0.8
        )
        logger.info("Generated narrative script successfully.")
        return {"narrative_script": response.choices[0].message.content}
    except Exception as e:
        logger.error(f"Error generating narrative: {e}")
        raise

# Main graph builder
def run_summary_agent(chunks: List[str]) -> str:
    """
    Build and execute a LangGraph workflow to summarize chunks and generate a narrative.

    Args:
        chunks: List of text chunks to summarize.

    Returns:
        The generated narrative script.

    Raises:
        ValueError: If chunks list is empty or invalid.
        RuntimeError: If graph execution fails.
    """
    if not chunks or not all(isinstance(chunk, str) for chunk in chunks):
        logger.error("Invalid or empty chunks provided.")
        raise ValueError("Chunks must be a non-empty list of strings.")

    try:
        # Initialize graph with shared state schema
        builder = StateGraph(SummaryState)

        # Add nodes
        builder.add_node("summarize_chunks", summarize_chunks)
        builder.add_node("generate_narrative", generate_narrative)

        # Define the flow
        builder.add_edge(START, "summarize_chunks")
        builder.add_edge("summarize_chunks", "generate_narrative")
        builder.add_edge("generate_narrative", END)

        # Compile and run
        graph = builder.compile()
        logger.info("LangGraph compiled successfully.")
        result = graph.invoke({"chunks": chunks})
        logger.info("Graph execution completed.")
        return result["narrative_script"]
    except Exception as e:
        logger.error(f"Error running summary agent: {e}")
        raise RuntimeError(f"Failed to execute summary agent: {e}")

