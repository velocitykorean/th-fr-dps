import os, sys, json, time, requests, re
import config

# Pre-crafted master curriculum for The Freudian Depths channel (Sigmund Freud psychoanalytic masterworks)
FREUD_CURRICULUM = [
    {
        "id": "ep_1",
        "topic": "The Architecture of the Unconscious: Id, Ego, and Superego",
        "focus": "A deep psychoanalytic examination of Freud's structural model of the mind: the primal drives of the Id, the conscious mediator of the Ego, and the ruthless moral tyranny of the Superego.",
        "thumbnail_title_1": "THE UNCONSCIOUS ID",
        "thumbnail_title_2": "EGO & GUILT",
        "thumbnail_hook": "The Secret War Inside Your Mind",
        "acts": [
            ("Act 1: The Iceberg of Consciousness", "The revelation that conscious awareness is merely the visible tip of an immense, submerged mental realm."),
            ("Act 2: The Id: The Boiling Cauldron of Desire", "Primal instincts, the pleasure principle, and the uncivilized biological drives that govern human action."),
            ("Act 3: The Ego: The Beleaguered Mediator", "Balancing the brutal demands of the Id against the harsh constraints of reality and survival."),
            ("Act 4: The Superego: The Internalized Tyrant", "The birth of guilt, the harsh judgment of the internalized father, and the psychological roots of neurosis."),
            ("Act 5: Psychoanalytic Awakening: Reclaiming the Unconscious", "Freud's famous dictum: 'Where Id was, there Ego shall be.' How self-knowledge liberates the human spirit.")
        ]
    },
    {
        "id": "ep_2",
        "topic": "The Interpretation of Dreams: The Royal Road to the Unconscious",
        "focus": "Unlocking Freud's magnum opus: how dreams serve as the masked fulfillments of repressed desires through condensation, displacement, and censorship.",
        "thumbnail_title_1": "SECRET OF DREAMS",
        "thumbnail_title_2": "UNCONSCIOUS DESIRE",
        "thumbnail_hook": "What Your Nightmares Really Mean",
        "acts": [
            ("Act 1: The Royal Road: Why We Dream", "The nocturnal theater of the soul and the collapse of daytime censorship."),
            ("Act 2: Manifest vs. Latent Content", "The dream as remembered versus the subterranean forbidden thoughts driving it."),
            ("Act 3: The Machinery of Dream-Work", "Condensation, displacement, and the symbolic language of the unconscious mind."),
            ("Act 4: Nightmares and the Compulsion to Repeat", "When dreams become crucibles of trauma and unresolved anxiety."),
            ("Act 5: The Interpreted Self: Deciphering the Riddle of Night", "How confronting dream-language reveals the hidden truth of our deepest emotional longing.")
        ]
    },
    {
        "id": "ep_3",
        "topic": "Defense Mechanisms: The Hidden Masks of the Human Ego",
        "focus": "How the ego shields itself from unbearable truths: repression, projection, rationalization, reaction formation, and sublimation.",
        "thumbnail_title_1": "DEFENSE MECHANISMS",
        "thumbnail_title_2": "WHY WE LIE",
        "thumbnail_hook": "How Your Mind Fools You",
        "acts": [
            ("Act 1: The Fortress of the Ego", "Why truth is often too painful to confront directly and the necessity of psychological armor."),
            ("Act 2: Repression and the Return of the Repressed", "Buried thoughts do not die; they are buried alive and fester into symptomatic suffering."),
            ("Act 3: Projection: Hating in Others What You Deny in Yourself", "The mirror of hostility and how we cast our darkest traits onto friends and enemies."),
            ("Act 4: Rationalization and Reaction Formation", "The sophisticated lies we tell ourselves to justify weakness, envy, and moral compromise."),
            ("Act 5: Sublimation: The Supreme Alchemy", "Channeling primitive libido and rage into monumental art, science, and civilization.")
        ]
    },
    {
        "id": "ep_4",
        "topic": "Civilization and Its Discontents: The High Price of Human Order",
        "focus": "Why human happiness is fundamentally incompatible with modern society: instinctual renunciation and universal guilt.",
        "thumbnail_title_1": "CIVILIZATION'S PRICE",
        "thumbnail_title_2": "MODERN NEUROSIS",
        "thumbnail_hook": "Why Society Makes Us Sick",
        "acts": [
            ("Act 1: The Tragic Bargain", "Renouncing primal freedom for safety and security."),
            ("Act 2: The Aggressive Instinct", "Homo homini lupus: man is a wolf to man."),
            ("Act 3: The Genesis of Modern Guilt", "How civilization turns aggression inward through the superego."),
            ("Act 4: The Neurotic Epidemic", "Why peace of order produces sickness of spirit."),
            ("Act 5: Beyond Discontent: The Courage of Conscious Existence", "Finding equilibrium between animal instinct and civilized restraint.")
        ]
    },
    {
        "id": "ep_5",
        "topic": "Beyond the Pleasure Principle: Eros and Thanatos (The Death Drive)",
        "focus": "The dark, subterranean instinct that competes with life: the human compulsion to repeat trauma and seek the stillness of nothingness.",
        "thumbnail_title_1": "EROS & THANATOS",
        "thumbnail_title_2": "THE DEATH DRIVE",
        "thumbnail_hook": "Why We Destroy What We Love",
        "acts": [
            ("Act 1: The Mystery of Repetition Compulsion", "Why do human beings return repeatedly to destructive relationships and pain?"),
            ("Act 2: The Pleasure Principle and Its Limits", "Recognizing that human behavior is not governed solely by the pursuit of pleasure."),
            ("Act 3: Thanatos: The Longing for Stillness", "The biological instinct of living matter to return to the peace of the inorganic state."),
            ("Act 4: The Clash of the Titans: Love vs. Destruction", "Eros binding humanity into community while Thanatos ceaselessly pulls it apart."),
            ("Act 5: The Affirmation of Eros", "How harnessing the life instinct shields humanity from self-annihilation.")
        ]
    },
    {
        "id": "ep_6",
        "topic": "The Psychology of Love, Attachment, and the Shadow of the Parent",
        "focus": "Why adult romantic attraction is an echo of childhood: transference, the idealization of the beloved, and unresolved caregiver wounds.",
        "thumbnail_title_1": "THE SHADOW OF LOVE",
        "thumbnail_title_2": "DESIRE & ATTACHMENT",
        "thumbnail_hook": "Why You Love Who You Love",
        "acts": [
            ("Act 1: Transference in Romance", "Falling in love not with a person, but with a childhood phantom."),
            ("Act 2: Narcissistic vs. Anaclitic Love", "Loving who you are versus loving who protects and nurtures you."),
            ("Act 3: The Madonna-Whore Dichotomy", "The tragic split between tenderness and sexual desire in human psychology."),
            ("Act 4: The Agony of Unrequited Devotion", "Why the ego surrenders its boundaries and identity to the beloved."),
            ("Act 5: Mature Intimacy: Unmasking the Beloved", "Seeing the partner truly, free from the projections of childhood ghosts.")
        ]
    },
    {
        "id": "ep_7",
        "topic": "The Oedipus Complex and the Buried Origins of Guilt",
        "focus": "The foundational psychoanalytic myth: childhood rivalry, the dread of castration, and the establishment of moral conscience.",
        "thumbnail_title_1": "BURIED GUILT",
        "thumbnail_title_2": "THE OEDIPAL SHADOW",
        "thumbnail_hook": "The Forbidden Truths of Childhood",
        "acts": [
            ("Act 1: The Tragedy of King Oedipus", "The mythic resonance of destiny, blind pride, and the unbearable truth of identity."),
            ("Act 2: The Primal Triangle: Child, Mother, and Father", "The dawn of jealousy, competition, and longing in the formative years."),
            ("Act 3: The Dread of Retaliation and Conscience", "How the fear of paternal retribution forces the internal consolidation of morals."),
            ("Act 4: Totem and Taboo: The Primal Clan", "The anthropological myth of the rebellious sons and the birth of universal law."),
            ("Act 5: Transcending the Complex", "Growing beyond the parental shadow into sovereign adulthood.")
        ]
    },
    {
        "id": "ep_8",
        "topic": "Sublimation: How Madness and Lust Become Art and Genius",
        "focus": "The supreme creative mechanism of the mind: transmuting raw libido and aggressive instincts into philosophy, art, and civilization.",
        "thumbnail_title_1": "ART OF SUBLIMATION",
        "thumbnail_title_2": "MADNESS TO GENIUS",
        "thumbnail_hook": "How Primal Desires Fuel Masterpieces",
        "acts": [
            ("Act 1: The Untamed Reservoir of Libido", "The primitive volcanic energy surging beneath human civilized behavior."),
            ("Act 2: When Repression Fails: Neurosis", "The tragic cost of merely suffocating instincts without providing an outlet."),
            ("Act 3: The Miracle of Sublimation", "How the mind redirects base drives toward cultural and intellectual heights."),
            ("Act 4: The Case of Leonardo da Vinci", "Freud's study of how maternal longing transformed into scientific and artistic perfection."),
            ("Act 5: The Sublimated Life: Crafting Beauty from Darkness", "Turning personal anguish and instinctual turmoil into enduring purpose.")
        ]
    },
    {
        "id": "ep_9",
        "topic": "The Psychopathology of Everyday Life: Slips of the Tongue and Hidden Truths",
        "focus": "Parapraxes, forgotten names, accidental blunders, and how the unconscious betrays our most guarded secrets in daily speech.",
        "thumbnail_title_1": "THE FREUDIAN SLIP",
        "thumbnail_title_2": "ACCIDENTS NEVER LIE",
        "thumbnail_hook": "What Your Tongue Betrays",
        "acts": [
            ("Act 1: There Are No Accidents in Mind", "The doctrine of psychic determinism: every word and slip has a cause."),
            ("Act 2: The Anatomy of the Slips of the Tongue", "How repressed hostility or forbidden desire hijacks the vocal cords."),
            ("Act 3: Forgetting Names and Intentions", "Why we forget the very things that cause unconscious conflict or pain."),
            ("Act 4: Bungled Actions and Accidental Losses", "Losing wedding rings and breaking gifts as unacknowledged psychic rebellion."),
            ("Act 5: The Transparent Mask: Listening to the Unconscious", "Developing psychoanalytic ear to understand what people truly mean.")
        ]
    },
    {
        "id": "ep_10",
        "topic": "Mourning and Melancholia: The Secret Anatomy of Grief and Depression",
        "focus": "The vital distinction between conscious mourning and pathological melancholia: turning unconscious rage inward against oneself.",
        "thumbnail_title_1": "MOURNING & LOSS",
        "thumbnail_title_2": "MELANCHOLIA",
        "thumbnail_hook": "Why Depression Attacks Self-Worth",
        "acts": [
            ("Act 1: The Pain of Severance", "How the psyche confronts the physical or emotional loss of a loved object."),
            ("Act 2: Normal Mourning: The Painful Withdrawal of Libido", "Releasing bonds bit by bit until the ego is once again free and uninhibited."),
            ("Act 3: Melancholia: When the Ego Attacks Itself", "The collapse of self-esteem, intense self-reproach, and delusion of worthlessness."),
            ("Act 4: The Shadow of the Object: Introjection", "Why the rage meant for the lost beloved is turned inward upon the self."),
            ("Act 5: Liberation from the Inner Executioner", "Reclaiming the ego from the clutches of buried resentment.")
        ]
    },
    {
        "id": "ep_11",
        "topic": "Totem and Taboo: The Primal Origins of Religion and Morality",
        "focus": "How ancient clan psychology, incest avoidance, and guilt over primal rebellion formed the universal bedrock of human culture.",
        "thumbnail_title_1": "TOTEM & TABOO",
        "thumbnail_title_2": "THE PRIMAL CRIME",
        "thumbnail_hook": "The Sacred Shadows of the Past",
        "acts": [
            ("Act 1: The Power of Taboo", "Forbidden actions that carry an unspoken, magnetic dread and attraction."),
            ("Act 2: The Primal Horde", "The tyranny of the dominant father and the gathering wrath of the sons."),
            ("Act 3: The Primal Feast and Remorse", "The slaying of the father and the genesis of retroactive obedience."),
            ("Act 4: The Totem Animal as Sacred Substitute", "Honoring and ritualizing the ancestor to appease unconscious guilt."),
            ("Act 5: The Eternal Re-enactment", "How modern institutions still reenact the primal drama of guilt and atonement.")
        ]
    },
    {
        "id": "ep_12",
        "topic": "The Future of an Illusion: Faith, Wish-Fulfillment, and the Search for Fatherly Protection",
        "focus": "Freud's controversial critique of religious dogmas as psychological wish-fulfillments born from childlike helplessness against nature and death.",
        "thumbnail_title_1": "THE GREAT ILLUSION",
        "thumbnail_title_2": "WISH & FEAR",
        "thumbnail_hook": "Why Man Invents Gods",
        "acts": [
            ("Act 1: The Terrors of Nature and Fate", "Human frailty before disease, earthquake, storm, and inexorable mortality."),
            ("Act 2: The Invention of Providence", "Personifying the universe into a protective father figure who rewards and punishes."),
            ("Act 3: The Psychology of Wish-Fulfillment", "Why an illusion is distinct from an error: belief born from intense emotional need."),
            ("Act 4: The Childish Fixation of Humanity", "Treating adulthood as a perpetual state of waiting for supernatural rescue."),
            ("Act 5: The Education to Reality", "Abandoning cosmic crutches and embracing science, reason, and self-reliance.")
        ]
    }
]

# Master pre-written script for Episode 1 (The Architecture of the Unconscious)
EPISODE_1_SCRIPT = [
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Welcome into the quiet, analytical sanctuary of The Freudian Depths. Today, we turn our gaze inward, beyond the polite surface of everyday awareness, into the vast and shadowy labyrinth of the human unconscious."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "For millennia, philosophy proclaimed that man is a rational animal, master of his own mind, sovereign over his choices, and architect of his moral destiny. But at the close of the nineteenth century, Sigmund Freud delivered a devastating blow to human narcissism."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Just as Copernicus displaced the earth from the center of the universe, and Darwin displaced man from his divine pedestal, Freud demonstrated that the ego is not master in its own house."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Consider the metaphor of the iceberg. What we call our conscious mind \u2014 the rational thoughts, the carefully reasoned arguments, the deliberate plans of our daytime life \u2014 represents merely the visible tip protruding above the cold waterline of awareness."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Beneath that waterline rests an immense, unseen mass: submerged desires, buried traumas, repressed instincts, and forgotten memories that continue to hum with volcanic energy, silently steering our lives while we remain blind to their presence."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "To map this subterranean topography, Freud developed his revolutionary structural model of the psyche. He divided the human soul not into harmonious virtues, but into three warring factions: the Id, the Ego, and the Superego."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Let us descend first into the primordial foundation: the Id. The Id is the biological inheritance of our species, the reservoir of instinctual energy that Freud termed the libido."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "It knows no logic, no time, no morality, and no contradictions. It operates exclusively under the Pleasure Principle \u2014 the absolute, uncompromising demand for immediate gratification and the discharge of tension."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "As Freud wrote: 'It is filled with energy reaching it from the instincts, but it has no organization, produces no collective will, but only a striving to bring about the satisfaction of the instinctual needs subject to the observance of the pleasure principle.'"
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "When a newborn enters the world, it is entirely Id. It screams for milk, for warmth, for touch, indifferent to the exhaustion of its mother or the laws of society. The Id remains within each of us throughout life \u2014 an untamed, amoral creature lurking behind our civilized attire."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "If humanity were governed solely by the Id, civilization would instantly collapse into a bloody carnival of unchecked aggression and unbridled appetite. Reality quickly forces a modification upon this boiling cauldron: the birth of the Ego."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "The Ego is that portion of the Id which has been altered by the direct influence of the external world through perception. It is the agent of reason, logic, and self-preservation."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Unlike the impulsive Id, the Ego operates under the Reality Principle. It does not abandon the search for pleasure, but postpones it, testing the environment to discover safe, socially viable pathways to satisfy our biological drives."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Freud famously compared the relation between the Ego and the Id to that of a rider upon a spirited horse. The horse provides the raw locomotive energy, but the rider retains the privilege of directing the course."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Yet, all too often, the rider finds himself compelled to guide his steed where it desires to go, disguising the animal's untamed impulse as his own rational decision."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "The Ego's position is fragile and tragic. It is an embattled mediator, struggling to maintain sanity while caught between three relentless masters: the external world, the insatiable Id, and the cruel tyranny of the Superego."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "This brings us to the third and most formidable structure of our inner architecture: the Superego. Where does morality truly come from? Is conscience a divine gift whispered from heaven, or is it a psychological artifact of human development?"
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "For Freud, the Superego is the internalized voice of parental authority, social rules, and cultural taboos. Through the painful resolution of childhood rivalries, the child internalizes the forbidding father and mother into the core of his own psyche."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "The Superego becomes an inner watchtower, observing every fleeting thought, every illicit fantasy, and every selfish desire with unblinking scrutiny."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Unlike the external law, which can only punish outward actions, the Superego punishes the Ego for mere intentions. You cannot conceal a secret from yourself. The moment an forbidden wish stirs in the Id, the Superego retaliates with crushing waves of unconscious guilt and anxiety."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "This explains the great paradox of human morality: the more virtuous and conscientious a person becomes, the more intensely he suffers from feelings of unworthiness, inadequacy, and guilt. His Superego has become an insatiable prosecutor."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "We see now why modern human beings are perpetually plagued by neurosis, anxiety, and internal exhaustion. We are walking battlefields, torn apart by the irreconcilable conflict between our animal biology and our civilized ideals."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "What is the psychoanalytic solution to this perpetual civil war? Freud was never a naive optimist. He did not promise effortless happiness or the eradication of suffering. He recognized that human life is inherently tragic and conflicted."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Yet, he offered humanity a noble and courageous goal: 'Where Id was, there Ego shall be.' Psychoanalysis is the patient, fearless work of reclaiming the reclaimed land from the dark ocean of the unconscious."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "As long as you remain ignorant of your unconscious drives, you will continue to call your fate what is merely your own repressed desire. You will choose destructive partners, repeat self-sabotaging habits, and endure mysterious anxieties without ever understanding why."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "True psychological maturity begins when you stop fleeing from your shadows. You must possess the intellectual honesty to acknowledge the volcanic appetites of your Id, and the moral courage to dismantle the irrational, punitive dogmas of your Superego."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Strengthen the Ego. Ground yourself in the sober assessment of reality. Learn to channel your passions through creative sublimation rather than suffocating repression."
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "For in the quiet words of Sigmund Freud: 'One day, in retrospect, the years of struggle will strike you as the most beautiful.'"
    },
    {
        "speaker": "male",
        "name": "The Psychoanalyst",
        "text": "Thank you for descending with us into The Freudian Depths. If this inquiry into the architecture of the human mind has illuminated the hidden corridors of your own soul, subscribe to our channel, share your thoughts in the comments below, and walk forward with fearless self-awareness. Until our next descent \u2014 know thyself."
    }
]

def load_history_topics() -> list:
    past = []
    for fname in ["published_videos.json", "history.json"]:
        fpath = os.path.join(config.BASE_DIR, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and item.get("topic"):
                                t = item["topic"].strip()
                                if t not in past:
                                    past.append(t)
            except Exception:
                pass
    return past

def generate_dynamic_story_ai(topic: str = None, ep_num: int = 1, past_topics: list = None) -> dict:
    """Uses Pollinations AI to dynamically generate a 100% original Freud episode."""
    if past_topics is None:
        past_topics = load_history_topics()

    print(f"[StoryGenerator] Invoking AI for dynamic psychoanalytic episode #{ep_num}...")
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("POLLINATIONS_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    avoid_clause = f"AVOID repeating these already covered topics: {', '.join(past_topics)}" if past_topics else ""

    prompt = f"""You are Sigmund Freud's intellectual heir and the lead psychoanalyst for 'The Freudian Depths' channel.
Generate a master 20-minute spoken philosophical video episode (Episode #{ep_num}).
{avoid_clause}
Topic override: {topic if topic else 'Choose a profound, unexamined theme from Freud (e.g. Id Ego Superego, The Interpretation of Dreams, Civilization and Its Discontents, Beyond the Pleasure Principle, Defense Mechanisms, Mourning and Melancholia)'}.

Return ONLY valid JSON matching this exact structure:
{{
  "topic": "Comprehensive Title of the Freudian Topic",
  "focus": "2-3 sentences explaining the core psychoanalytic inquiry.",
  "thumbnail_title_1": "2-4 WORDS HEADLINE 1 (e.g. THE UNCONSCIOUS ID)",
  "thumbnail_title_2": "2-4 WORDS HEADLINE 2 (e.g. EGO & GUILT)",
  "thumbnail_hook": "Short curiosity question (e.g. The Secret War Inside Your Mind)",
  "acts": [
    ["Act 1: Title", "Summary"],
    ["Act 2: Title", "Summary"],
    ["Act 3: Title", "Summary"],
    ["Act 4: Title", "Summary"],
    ["Act 5: Title", "Summary"]
  ],
  "dialogue": [
    {{"speaker": "male", "name": "The Psychoanalyst", "text": "Deep, clinical, aristocratic psychoanalytic narration in the contemplative cadence of Sigmund Freud..."}}
  ]
}}
Ensure the dialogue contains at least 30 to 35 rich turns (~2,200 words total) divided evenly across the 5 acts.
"""

    try:
        r = requests.post(
            "https://text.pollinations.ai/",
            json={"messages": [{"role": "user", "content": prompt}], "jsonMode": True},
            headers=headers,
            timeout=90
        )
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict) and data.get("dialogue") and len(data["dialogue"]) >= 15:
                print(f"[StoryGenerator] AI successfully generated {len(data['dialogue'])} turns for '{data.get('topic')}'.")
                return data
    except Exception as e:
        print(f"[StoryGenerator] AI generation encountered issue ({e}). Proceeding to curriculum...")

    return None

def generate_full_podcast_story(target_minutes: float = 20.0, topic: str = None, ep_num: int = 1) -> dict:
    """Generates the full story dialogue and chapter structure for the episode."""
    print(f"[StoryGenerator] Preparing script for Episode #{ep_num} (Target: {target_minutes:.1f} mins)...")
    past_topics = load_history_topics()

    # 1. Select matching or next unperformed curriculum catalog item
    catalog_item = None
    if topic:
        catalog_item = next((item for item in FREUD_CURRICULUM if item["topic"].lower() == topic.lower() or item["id"] == topic), None)

    if not catalog_item:
        ep_id = f"ep_{ep_num}"
        match_by_id = next((item for item in FREUD_CURRICULUM if item["id"] == ep_id), None)
        if match_by_id and match_by_id["topic"] not in past_topics:
            catalog_item = match_by_id

    if not catalog_item:
        for item in FREUD_CURRICULUM:
            if item["topic"] not in past_topics:
                catalog_item = item
                break

    if not catalog_item:
        curriculum_idx = (ep_num - 1) % len(FREUD_CURRICULUM)
        catalog_item = FREUD_CURRICULUM[curriculum_idx]

    # 2. Select or generate full dialogue
    dialogue = None
    if catalog_item["id"] == "ep_1":
        dialogue = EPISODE_1_SCRIPT
    else:
        ai_story = generate_dynamic_story_ai(topic=catalog_item["topic"], ep_num=ep_num, past_topics=past_topics)
        if ai_story and ai_story.get("dialogue"):
            catalog_item["thumbnail_title_1"] = ai_story.get("thumbnail_title_1", catalog_item["thumbnail_title_1"])
            catalog_item["thumbnail_title_2"] = ai_story.get("thumbnail_title_2", catalog_item["thumbnail_title_2"])
            catalog_item["thumbnail_hook"] = ai_story.get("thumbnail_hook", catalog_item["thumbnail_hook"])
            dialogue = ai_story["dialogue"]

    if not dialogue:
        dialogue = EPISODE_1_SCRIPT

    # Map chapters to dialogue turns
    total_turns = len(dialogue)
    turns_per_act = max(1, total_turns // 5)
    chapters = []
    for act_idx, act_info in enumerate(catalog_item["acts"]):
        start_turn = min(act_idx * turns_per_act, total_turns - 1)
        chapters.append({
            "act": act_idx + 1,
            "title": act_info[0],
            "description": act_info[1],
            "start_turn": start_turn,
            "start_time": 0.0
        })

    total_words = sum(len(t["text"].split()) for t in dialogue)
    print(f"[StoryGenerator] Dialogue assembled: {len(dialogue)} turns, {total_words} words.")
    est_duration_mins = (total_words / 130.0) + (len(dialogue) * config.PAUSE_BETWEEN_TURNS / 60.0)
    print(f"[StoryGenerator] Estimated spoken duration: ~{est_duration_mins:.1f} minutes.")

    return {
        "episode": ep_num,
        "topic": catalog_item["topic"],
        "focus": catalog_item["focus"],
        "thumbnail_title_1": catalog_item["thumbnail_title_1"],
        "thumbnail_title_2": catalog_item["thumbnail_title_2"],
        "thumbnail_hook": catalog_item["thumbnail_hook"],
        "chapters": chapters,
        "dialogue": dialogue
    }

def generate_metadata(topic: str, total_duration_sec: float, chapters: list, ep_num: int = 1, story: dict = None) -> dict:
    """Formats dynamic YouTube title, timestamps description, tags, and metadata."""
    if story and story.get("focus"):
        focus_desc = story["focus"]
    else:
        focus_desc = f"Sigmund Freud's profound psychoanalytic inquiry into {topic}."

    clean_topic = topic.replace("Sigmund Freud on ", "").replace("Sigmund Freud: ", "")
    title = f"Sigmund Freud: {clean_topic} | Deep Psychoanalysis & The Unconscious (Ep. {ep_num:02d})"
    if len(title) > 98:
        title = f"Sigmund Freud: {clean_topic[:60]}... (Ep. {ep_num:02d})"

    desc_lines = [
        f"{focus_desc}",
        "",
        '"The mind is like an iceberg, it floats with one-seventh of its bulk above water."',
        " — Sigmund Freud",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "TIMESTAMPS & CHAPTERS:",
    ]

    for ch in chapters:
        sec = int(ch.get("start_time", 0.0))
        mm = sec // 60
        ss = sec % 60
        desc_lines.append(f"{mm:02d}:{ss:02d} - {ch['title']}")

    desc_lines.extend([
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "ABOUT THE FREUDIAN DEPTHS:",
        "The Freudian Depths is dedicated to exploring the uncharted corridors of the unconscious mind, human desire, defense mechanisms, and the hidden psychological architecture that governs our civilization.",
        "",
        "Subscribe to join our psychoanalytic circle: @TheFreudianDepths",
        "",
        "RECOMMENDED FREUD READINGS:",
        "• The Ego and the Id (1923)",
        "• The Interpretation of Dreams (1899)",
        "• Civilization and Its Discontents (1930)",
        "• Beyond the Pleasure Principle (1920)",
        "• The Psychopathology of Everyday Life (1901)",
        "• Totem and Taboo (1913)",
        "",
        f"#Freud #Psychoanalysis #Psychology #Unconscious #Ego #Id #Superego #Dreams #MentalHealth #DeepThinking"
    ])

    return {
        "title": title,
        "description": "\n".join(desc_lines),
        "tags": [
            "Sigmund Freud", "Freud", clean_topic, "Psychoanalysis", "Psychology", "Unconscious Mind",
            "The Ego and the Id", "Interpretation of Dreams", "Civilization and Its Discontents",
            "Defense Mechanisms", "Deep psychology", "Wisdom", "Freudian Depths"
        ]
    }
