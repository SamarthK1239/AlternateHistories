"""
Historical scenarios for the alternate history application.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class HistoricalScenario:
    """Represents a historical scenario with alternate possibilities."""
    
    name: str
    description: str
    time_period: str
    initial_situation: str

# Available scenarios
AVAILABLE_SCENARIOS: Dict[str, HistoricalScenario] = {
    "library_alexandria": HistoricalScenario(
        name="The Library of Alexandria",
        description="What if the great Library of Alexandria was never destroyed?",
        time_period="48 BCE - 641 CE",
        initial_situation=(
            "You are the head librarian of the Great Library of Alexandria in 48 BCE. "
            "Julius Caesar's forces have accidentally started a fire that threatens to spread "
            "to the library district. You must decide how to protect the world's greatest "
            "collection of knowledge while the city burns around you."
        )
    ),
    
    "mongol_europe": HistoricalScenario(
        name="Mongol Invasion of Europe",
        description="What if the Mongols had successfully conquered all of Europe?",
        time_period="1241 CE",
        initial_situation=(
            "You are Ögedei Khan, son of Genghis Khan, and your Mongol forces have just "
            "crushed European armies at Mohi and Legnica. All of Europe lies open before you, "
            "but news arrives that forces you to make a crucial decision about the future "
            "of your western campaign."
        )
    ),
    
    "columbus_pacific": HistoricalScenario(
        name="Columbus Sails West to Asia",
        description="What if Columbus had actually reached Asia by sailing west?",
        time_period="1492 CE",
        initial_situation=(
            "You are Christopher Columbus, and after months at sea, you've finally reached "
            "what you believe to be the Indies. However, the lands and peoples you encounter "
            "are unlike anything described by Marco Polo. You must decide how to proceed "
            "with your mission while managing increasingly restless crew members."
        )
    ),
    
    "black_death": HistoricalScenario(
        name="The Black Death Prevention",
        description="What if medieval physicians had understood disease transmission?",
        time_period="1347 CE",
        initial_situation=(
            "You are a physician in the port city of Genoa when ships arrive carrying "
            "a mysterious plague from the East. Unlike your contemporaries, you suspect "
            "this disease spreads through contact rather than 'bad air.' You must convince "
            "the city authorities to take unprecedented quarantine measures."
        )
    ),
    
    "archduke_survives": HistoricalScenario(
        name="Archduke Franz Ferdinand Lives",
        description="What if the assassination of Archduke Franz Ferdinand had failed?",
        time_period="June 28, 1914",
        initial_situation=(
            "You are Archduke Franz Ferdinand of Austria-Hungary, and you've just survived "
            "an assassination attempt in Sarajevo. Your driver took a wrong turn, but your "
            "quick thinking saved your life when Gavrilo Princip's shot missed. As tensions "
            "rise across Europe, you must decide how to respond to this act of Serbian nationalism "
            "while your empire teeters on the brink of war."
        )
    ),
    
    "lusitania_warning": HistoricalScenario(
        name="The Lusitania's Final Voyage",
        description="What if the Lusitania had heeded Germany's submarine warnings?",
        time_period="May 7, 1915",
        initial_situation=(
            "You are Captain William Turner of the RMS Lusitania. German U-boats have been "
            "attacking ships in these waters, and you've received warnings about submarine "
            "activity. Your ship carries 1,962 passengers and crew, including many Americans. "
            "You must decide whether to alter course, reduce speed for safety, or maintain "
            "schedule despite the submarine threat off the Irish coast."
        )
    ),
    
    "zimmermann_intercepted": HistoricalScenario(
        name="The Zimmermann Telegram Plot",
        description="What if Germany's secret alliance offer to Mexico had succeeded?",
        time_period="January 1917",
        initial_situation=(
            "You are Foreign Secretary Arthur Zimmermann of Germany. Your secret telegram "
            "proposing a German-Mexican alliance against the United States has been sent, "
            "but you're unaware that British intelligence has intercepted it. Mexico shows "
            "interest in your offer of reclaiming Texas, New Mexico, and Arizona. You must "
            "decide how to proceed with this alliance while managing the risk of bringing "
            "America into the European war."
        )
    ),
    
    "hitler_art_school": HistoricalScenario(
        name="The Rejected Artist's Path",
        description="What if Adolf Hitler had been accepted into art school?",
        time_period="September 1907",
        initial_situation=(
            "You are the admissions director of the Vienna Academy of Fine Arts. A passionate "
            "young man named Adolf Hitler from Austria has applied for the second time after "
            "being rejected last year. His artwork shows some talent but lacks technical skill. "
            "However, his determination is evident. You must decide whether to give him another "
            "chance, knowing that this decision could alter the path of a future political figure."
        )
    ),
    
    "pearl_harbor_warning": HistoricalScenario(
        name="The Pearl Harbor Intelligence",
        description="What if the US had acted on early warnings about Pearl Harbor?",
        time_period="December 6, 1941",
        initial_situation=(
            "You are Admiral Husband Kimmel, commander of the US Pacific Fleet at Pearl Harbor. "
            "Intelligence reports suggest increased Japanese naval activity, and you've received "
            "vague warnings about possible attacks. However, Washington believes any Japanese "
            "action will target the Philippines or Southeast Asia. With limited resources and "
            "conflicting intelligence, you must decide how to position your fleet and defenses "
            "for the next 24 hours."
        )
    ),
    
    "operation_barbarossa": HistoricalScenario(
        name="Stalin's Dilemma",
        description="What if Stalin had believed the warnings about German invasion?",
        time_period="June 20, 1941",
        initial_situation=(
            "You are Joseph Stalin, and multiple intelligence sources are warning that Germany "
            "is about to break the Molotov-Ribbentrop Pact and invade the Soviet Union. Your "
            "generals urge mobilization, but you fear that aggressive preparations might provoke "
            "Hitler into an attack he's not actually planning. German troops are massing on "
            "your border, but diplomatic channels remain open. You must decide whether to fully "
            "mobilize the Red Army or maintain the non-aggression pact."
        )
    ),
    
    "d_day_weather": HistoricalScenario(
        name="D-Day: The Weather Decision",
        description="What if Operation Overlord had been postponed due to weather?",
        time_period="June 4, 1944",
        initial_situation=(
            "You are General Dwight D. Eisenhower, Supreme Allied Commander. Operation Overlord, "
            "the invasion of Normandy, is scheduled for tomorrow, but meteorologists predict "
            "terrible weather - high winds and rough seas that could doom the operation. "
            "Postponing means losing the element of surprise and risking German reinforcements. "
            "The tides won't be favorable again for weeks. You must decide whether to proceed "
            "with the invasion despite the weather or postpone and risk the consequences."
        )
    )
}

def get_scenario_list() -> Dict[str, str]:
    """Get a simple list of scenario names and descriptions."""
    return {key: scenario.description for key, scenario in AVAILABLE_SCENARIOS.items()}