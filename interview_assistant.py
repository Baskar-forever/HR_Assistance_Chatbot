import os
import logging
from typing import List, Dict
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class InterviewAssistant:
    """
    A class to handle the initial screening process for candidates using a conversational AI model.

    Attributes:
        llm (ChatMistralAI): The language model used for generating responses.
    """

    def __init__(self):
        """
        Initializes the InterviewAssistant class by setting up the language model.
        """
        logging.info("Initializing InterviewAssistant...")
        self.llm = ChatMistralAI(
            model="mistral-large-latest",
            api_key=os.getenv("MISTRAL_API_KEY"),  # API key loaded from environment variables
            temperature=0.1,  # Controls randomness in responses
            max_retries=2,  # Number of retries for failed requests
        )
        logging.info("InterviewAssistant initialized successfully.")

    def interview_process_by_assistant(self, question: str, history: List[Dict[str, str]]) -> str:
        """
        Handles the interview process by generating responses based on the candidate's input and conversation history.

        Args:
            question (str): The candidate's input question or response.
            history (List[Dict[str, str]]): The conversation history between the assistant and the candidate.

        Returns:
            str: The assistant's response to the candidate.
        """
        logging.info("Generating response for the candidate...")
        
        # Define the prompt template for the interview assistant
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """Your are the hr assitant for talentScount you will be assit for inizial screening.Your task is gather information from candidate one by one and one of the information[First show the details that could be ask then ask one by one] is tech stack ask 3 or 4 technical questions to canditate based on tech stack and ask technical questions one by one analyze the converstation histroy for maintain correct flow woth candidate.Once the inizial screening process completely done ending greeting with we cantact throw your email for the canditate.After the process candidate give any ending grettings like Thankyou response to this

                Information you need to gather:
                  Full Name
                  Email Address
                  Phone Number
                  Years of Experience
                  Desired Position(s)
                  Current Location
                  Tech Stack


                Return Format Should be like this:
                      {{
                        "full_name": "string",
                        "email": "string",
                        "phone_number": "string",
                        "years_of_experience": "string",
                        "desired_position": "string",
                        "current_location": "string",
                        "tech_stack": "string"
                        "technical_questions_and_answers": [{{"question1":"answer1","question2":"answer2","question3":"answer3"}}]
                      }}

                Example for technical question based on tech stack:
                  example tech stack: programming languages, frameworks, databases, and tools they are proficient in.
                  you need ask technical questions from this skills one by one

                Thinks to be reminder:
                    analyse history for maintain correct flow with candidate
                    first[staring] show what are the information you need ask then ask one by one information
                    provide meaningful responses do not have string like this "[Provide your answer or name...]
                    once all the process completed give end greetings.
                    We follow all GDPR guidelines to protect your privacy so candidate not intersted to share this information give end greetings.
                """,
            ),
            ("human", "{candidate_input}  {history}",)
        ])
        
        # Combine the prompt with the language model
        chain = prompt | self.llm
        
        try:
            # Invoke the chain with the candidate's input and conversation history
            llm_response = chain.invoke(
                {
                    "candidate_input": question,
                    "history": history,
                }
            )
            result = llm_response.content
            logging.info("Response generated successfully.")
            return result
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "An error occurred while processing your request. Please try again."
