from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, ConfigurableField
from langchain_core.tools import tool
from typing import Literal
from threat_detection_score.input_sanitizer.sanitize import sanitize_input
import json, textwrap, typer
from pprint import pprint

app = typer.Typer()


@app.command()
def main(
    human_message_input: str = typer.Option(
        ...,  # This indicates the option is required
        "--human-message-input",  # Specify the flag name
        "-i",  # Optional shorthand flag
        help="The input message describing the cybersecurity detection scenario.",
        callback=sanitize_input  # Use the sanitize_input function for validation
    ),
    temperature: str = typer.Option(
        0.0,  # Default value
        "--temperature",  # Specify the flag name
        help="The temperature of the LLM."
    ),
    model_name: str = typer.Option(
        "gpt-4o-mini",  # Default value
        "--model-name",  # Specify the flag name
        help="The LLM model used."
    ),
    max_retries: str = typer.Option(
        3,  # Default value
        "--max-retries",  # Specify the flag name
        help="The maximum number of retries for the LLM."
    )
):

    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_prompt}"),
            ("human", "{detection_requirement}"),
        ]
    )

    system_prompt = """
    You are a cybersecurity threat analyst tasked with evaluating threats to an organization. Your goal is to determine the appropriate threat score based on specific detection requirements and organizational context. Use the following guidelines to assign the correct score to each threat:

    - **Score 0:** Assign this score if the threat is irrelevant to the organization. Examples include threats targeting technologies, software, or sectors not used or operated by the organization, such as malware for a different operating system, attacks on unused software, or threats specific to industries or geographies irrelevant to the organization.

    - **Score 1:** Use this score for threats that are unlikely to target the organization directly, but a risk still exists. This includes threats from actors focusing on different geographies or sectors, emerging malware trends not yet seen in the organization's region, or attacks on less critical, seldom-used software.

    - **Score 2:** This score is for widespread or untargeted threats that affect a broad range of entities indiscriminately. Examples include mass phishing campaigns, generalized ransomware attacks, DDoS attacks without a specific target, and other campaigns that do not single out any specific industry or organization.

    - **Score 3:** Assign this score to threats that specifically target the organization. This includes known threats based on internal observations, targeted spear-phishing, attacks by APT groups known to target the sector, ransomware exploiting network vulnerabilities unique to the organization, and any other threat explicitly designed to affect the organization, its employees, or its operations directly.

    - **Score Chart Example:**

    | Score | Description                                                       | Examples                                                                                                                                                                                                                          |
    |-------|-------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | 0     | The threat is irrelevant to the organization.                      | 1. A threat targeting macOS endpoints in a Windows-only environment.<br>2. Linux ransomware in a Windows-dominated environment.<br>3. Mobile-focused malware when the organization does not use mobile devices for operations.<br>4. An attack leveraging a vulnerability in software the organization does not use.<br>5. Threats specific to hardware the organization has phased out.<br>6. Sector-specific attacks irrelevant to the organization's industry.<br>7. Geographically focused attacks outside the organization's area of operation.<br>8. Attacks on technologies the organization has no plans to adopt.<br>9. Threat actors known to only target individuals, not corporations.<br>10. Specific social engineering scams irrelevant to the organization's communication channels. |
    | 1     | The threat is likely not going to target your organization but the risk still exists. | 1. A threat actor primarily focused on targeting a geography outside your own but known to target your industry.<br>2. Emerging malware trends not yet seen in your region but prevalent in others.<br>3. Threats targeting industries similar to yours but not directly related.<br>4. Cyber campaigns focused on larger entities while you operate a small to medium business.<br>5. Generic phishing campaigns not tailored to your sector.<br>6. Attacks leveraging vulnerabilities in less critical software your organization seldom uses.<br>7. Information-stealing malware primarily targeting consumer data when your organization deals with B2B.<br>8. Threat actors known for espionage in sectors adjacent to yours.<br>9. Ransomware gangs historically targeting public institutions, and your business is private.<br>10. Insider threat tactics mainly reported in industries with high employee churn, which does not apply to your organization. |
    | 2     | The threat is widespread/untargeted.                               | 1. A mass Emotet malspam campaign.<br>2. Widespread phishing attempts not targeting any specific industry.<br>3. Generalized ransomware attacks seeking to exploit common vulnerabilities.<br>4. Broad DDoS attacks aimed at disrupting services indiscriminately.<br>5. Malvertising campaigns affecting a wide range of users.<br>6. Cryptojacking efforts exploiting widespread web platform vulnerabilities.<br>7. SQL injection attacks targeting websites regardless of their content or owner.<br>8. Credential stuffing attacks using previously breached databases.<br>9. Scareware campaigns aiming to dupe less tech-savvy users.<br>10. Watering hole attacks not specific to one sector or industry. |
    | 3     | The threat specifically targets your organization.                | 1. Known threat based on internal observations or a threat actor known to target your geography and industry.<br>2. Spear-phishing emails tailored to your organization's employees.<br>3. Advanced persistent threat (APT) groups with a history of targeting your sector.<br>4. Ransomware customized to exploit your organization's specific network vulnerabilities.<br>5. Insider threats with knowledge of your organization's systems and data.<br>6. Social engineering attacks designed around your corporate culture.<br>7. Competitor-driven espionage targeting your intellectual property.<br>8. Supply chain attacks aimed at software or services your organization relies on.<br>9. Threats exploiting recently disclosed vulnerabilities before your organization can patch them.<br>10. Targeted DDoS attacks aiming to disrupt your specific online services. |

    Analyze the detection inputs provided, considering the organization’s technology stack, industry sector, geographical location, and any specific vulnerabilities or previous threat encounters. Based on these factors and the guidelines above, assign an appropriate threat score and justify your reasoning. Consider the potential impact, the likelihood of the threat targeting the organization, and any recent trends or intelligence reports that might influence the threat level.
    {org_align_add_info}
    """


    prompt = chat_template.partial(system_prompt=system_prompt)


    add_on_info = """
    | Type                  | Value               |
    |-----------------------|---------------------|
    | technology stack      | ubuntu              |
    | technology stack      | linux               |
    | technology stack      | android             |
    | technology stack      | Windows Server 2019 |
    | technology stack      | windows 11          |
    | technology stack      | windows 10          |
    | technology stack      | mac os              |
    | technology stack      | iOS                 |
    | industry sector       | hospital            |
    | industry sector       | healthcare          |
    | industry sector       | soho                |
    | geographical location | north america       |
    | geographical location | michigan            |
    """

    prompt = prompt.partial(org_align_add_info=add_on_info)

    model = ChatOpenAI(model=model_name, temperature=temperature, max_retries=max_retries)

    @tool
    def org_alingment(score: Literal[0, 1, 2, 3], reason: str) -> None:
        """organizational alignment cyber security risk scoring"""
        pass

    tools = [org_alingment]

    chain = (
        {"detection_requirement": RunnablePassthrough()}
        | prompt
        | model.bind_tools(tools, tool_choice="org_alingment")
    )

    llm_result = chain.invoke({"detection_requirement": human_message_input})

    score = llm_result.tool_calls[0]["args"]["score"]
    reason = llm_result.tool_calls[0]["args"]["reason"]

    result = {
    "score": score,
    "reason": "\n".join(textwrap.wrap(reason, width=80)),
    "type": "organizational alignment"
    }

    print(json.dumps(result))

if __name__ == "__main__":
    app()