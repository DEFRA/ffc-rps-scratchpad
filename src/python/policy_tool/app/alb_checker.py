import autogen
from autogen_config import gpt4_config

user_proxy = autogen.UserProxyAgent(
    name="admin",
    system_message=f"""You coordinate the tasks.

    You take a user input which is a plain text document written in prose.
    And run it through the below workflow to each member from organisations, with the aim of identifying which aspects of the document will be of interest to that member.

    Workflow:
    - Identify whether the document applies to the organisation being assessed. It is perfectly acceptable if it is not.
    - Identify which specific sections of the document the organisation is interested in. Quote the section of the document.
    - For each quoted section, explain why the organisation will be interested in the document

    The current list of organisations is: ['Natural England', 'Forestry Commission', 'Animal and Plant Health Agency', 'Centre for Environment, Fisheries and Aquaculture Science', 'Environment Agency', 'Marine Management Organisation']

    One you have all the feedback from each expert and thier organisation summarise any repeat sections between multiple organisations - but highlight which organisations are impacted and why.
    And return all areas the organisation thought needed rework. We are particularly interested in overlaps between agencies so please highlight those.

    Finally - output a list of the organisation which have highlighted they are impacted.

    Once you have collected feedback from everyobe - submit "TERMINATE" into the chain.
    """,
    human_input_mode = "NEVER",
    llm_config=gpt4_config,
    code_execution_config=False,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
)

organisation_template = '''You are the specialist from an organisation.
    You read the user submitted document and output whether based on the description of your organisation you are impacted by the document.
    It is perfectly fine to say your are not impacted, but we are looking for broad views so if there is anything related please mention it.

    If you are impacted, quote which sections of the document you are interested in.
    - Explain why you are interested in that section.
    - Output each specific section as a numbered point, with the explaination being text under that point. Make separate explainations for each section.

    Below is a description of your organisation (from a markdown file):'''


organisation_natural_england = autogen.AssistantAgent(
    name="organisation_natural_england",
    llm_config=gpt4_config,
    system_message=f'''{organisation_template}
# Natural England
## Role:
This body is focused on conserving and enhancing the natural environment, including biodiversity and landscapes.
## Current Aims:
Natural England aims to improve habitat conservation, increase access to nature, and promote environmental stewardship.
## Environmental Impact:
By protecting species and habitats, Natural England contributes to maintaining biodiversity and enhancing ecosystem services.
## Expectations from Farmers and Landowners:
Natural England promotes the adoption of agri-environment schemes that support wildlife-friendly farming and habitat restoration.
''',
)

organisation_forestry_commission = autogen.AssistantAgent(
    name="organisation_forestry_commission",
    llm_config=gpt4_config,
    system_message=f'''{organisation_template}
    Below is a description of your organisation (from a markdown file):
## Forestry Commission
# Role:
The Forestry Commission is responsible for protecting, expanding, and promoting the sustainable management of woodlands and forests.
# Current Aims:
Increasing woodland cover, promoting sustainable forestry practices, and enhancing the role of forests in combating climate change are key priorities.
## Environmental Impact:
The Commission's work supports carbon sequestration, biodiversity conservation, and flood mitigation through sustainable forest management.
## Expectations from Farmers and Landowners:
Farmers and landowners are encouraged to plant trees, manage woodlands sustainably, and participate in afforestation initiatives.
''',
)

organisation_animal_and_plant_health_agency  = autogen.AssistantAgent(
    name="organisation_animal_and_plant_health_agency",
    llm_config=gpt4_config,
    system_message=f'''{organisation_template}
# Animal and Plant Health Agency (APHA)
## Role:
APHA safeguards animal and plant health, ensuring food safety and biosecurity in England.
## Current Aims:
Key objectives include preventing the spread of animal diseases, regulating veterinary medicines, and protecting crops from pests and diseases.
## Environmental Impact:
APHA's work contributes to the sustainable management of agricultural resources and protects ecosystems from invasive species.
## Expectations from Farmers and Landowners:
APHA expects compliance with biosecurity measures, responsible use of veterinary products, and participation in disease control programs.
''',
)

organisation_environment_fisheries_aquaculture  = autogen.AssistantAgent(
    name="organisation_environment_fisheries_aquaculture",
    llm_config=gpt4_config,
    system_message=f'''{organisation_template}
# Centre for Environment, Fisheries and Aquaculture Science (CEFAS)
## Role:
CEFAS provides scientific advice on marine and freshwater environments.
## Current Aims:
The agency focuses on supporting sustainable fisheries, understanding climate change impacts, and protecting aquatic environments.
## Environmental Impact:
CEFAS's research underpins policies that aim to protect marine biodiversity and support sustainable aquaculture.
## Expectations from Farmers and Landowners:
CEFAS works with stakeholders in the aquaculture industry to promote practices that minimize environmental impacts.
''',
)


marine_management_organisation  = autogen.AssistantAgent(
    name="marine_management_organisation",
    llm_config=gpt4_config,
    system_message=f'''{organisation_template}
# Marine Management Organisation (MMO)
## Role:
MMO manages England's marine resources, balancing conservation and economic activities.
## Current Aims:
The MMO focuses on sustainable fisheries, protecting marine habitats, and regulating marine development.
## Environmental Impact:
By ensuring sustainable use of marine resources, the MMO helps maintain healthy marine ecosystems.
## Expectations from Farmers and Landowners:
While more relevant to coastal landowners, the MMO encourages responsible land use that doesn't negatively impact marine environments, such as preventing runoff that could contribute to marine pollution.
''',
)

organisation_environment_agency  = autogen.AssistantAgent(
    name="organisation_environment_agency",
    llm_config=gpt4_config,
    system_message=f'''{organisation_template}
# Environment Agency (EA)
## Role:
The EA is responsible for protecting and improving the environment in England. It oversees flood defenses, manages water resources, regulates pollution, and monitors environmental quality.
## Current Aims:
Its current goals include tackling climate change impacts, enhancing biodiversity, and improving water quality.
## Environmental Impact:
The EA plays a significant role in mitigating environmental risks, reducing pollution, and ensuring sustainable use of natural resources.
## Expectations from Farmers and Landowners:
The EA encourages sustainable farming practices, efficient water usage, and compliance with regulations to reduce pollution and protect natural habitats.
''',
)

groupchat = autogen.GroupChat(agents=[user_proxy,
                                    organisation_natural_england,
                                    organisation_forestry_commission,
                                    organisation_animal_and_plant_health_agency,
                                    organisation_environment_fisheries_aquaculture,
                                    organisation_environment_agency,
                                    marine_management_organisation],
                            messages=[],
                            admin_name = user_proxy,
                            max_round=10)

def process(input_text: str, groupchat: autogen.GroupChat):
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

    chatresult = user_proxy.initiate_chat(
        manager,
        message=f"""run the worklow and output feedback for the following document: {input_text}'''
        """,
        silent=True)

    return chatresult