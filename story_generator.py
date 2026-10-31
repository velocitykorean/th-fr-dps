import os, sys, json, time, requests, re, hashlib
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
EPISODE_1_SCRIPT = [{'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Welcome into the quiet, analytical sanctuary of The Freudian Depths. Today, we turn our gaze inward, beyond the polite, polished surfaces of conscious awareness, into the vast, dark, and turbulent labyrinth of the human unconscious mind.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'For thousands of years, Western civilization comforted itself with the noble illusion that man is fundamentally a rational being. From the classical philosophers of ancient Athens to the thinkers of the Enlightenment, it was assumed that reason is the sovereign captain of the soul, that our thoughts are transparent to ourselves, and that our deliberate wills govern our moral destinies.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Yet, at the turn of the twentieth century, in a modest consulting room at Berggasse 19 in Vienna, Sigmund Freud delivered an intellectual earthquake that permanently shattered this vanity. He observed that throughout the history of human thought, our collective self-love has suffered three monumental, shattering wounds.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'The first was cosmological: Nicolaus Copernicus demonstrated that our earth is not the proud, immobile center of creation, but merely a wandering speck of dust orbiting an indifferent sun in infinite space. The second was biological: Charles Darwin proved that humanity was not created separate from nature, but descended through unyielding animal ancestry from the primates.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'And the third, and most excruciatingly personal wound, was psychological: Freud demonstrated through years of clinical investigation that the conscious human ego is not even master in its own house. What we consider our conscious mind is largely an observer, desperately attempting to rationalize forces it cannot see.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'To visualize this profound reality, Freud offered humanity one of the most enduring metaphors in all of psychological science: the iceberg. The conscious mind — the immediate thoughts we can articulate, the logical equations we balance, the deliberate social courtesies we exchange — represents merely the exposed tip protruding above the freezing waterline of perception.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Beneath that cold, shimmering surface lies the overwhelming bulk of the psyche: the vast subterranean expanse of the unconscious. Here reside our primal biological instincts, unresolved childhood conflicts, buried traumas, and forbidden longings that continue to hum with volcanic energy, silently steering our life choices while we remain completely oblivious to their command.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'This leads us to the supreme foundational dogma of psychoanalysis: the doctrine of psychic determinism. Nothing in the human mind happens by pure chance. Every slip of the tongue, every forgotten appointment, every sudden flash of unreasonable jealousy, and every recurrent nightmare is a carefully coded emissary from this submerged world, knocking on the doors of our conscious awareness.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'In 1923, after decades of clinical practice, Freud recognized that the simple division between conscious and unconscious was insufficient to explain the violent conflicts tearing human beings apart. In his seminal work, The Ego and the Id, he introduced his revolutionary structural model of the psyche: the Id, the Ego, and the Superego.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "Let us descend first into the most archaic, primordial foundation of our mental life: the Id, or das Es — the 'It'. The Id is the biological bedrock of our personality, the raw genetic inheritance of millions of years of evolutionary struggle. It is the deep volcanic core from which all psychological energy originates."}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "Freud famously described the Id as a 'cauldron full of seething excitations.' It knows no laws of logic, no passage of time, no morality, no good, and no evil. Within the Id, mutually contradictory impulses and violent paradoxes exist side by side for decades without ever neutralizing or moderating one another."}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'The Id is governed unconditionally by what Freud termed the Pleasure Principle. It is driven by an insatiable, uncompromising demand for the immediate discharge of instinctual tension. The Id seeks gratification without postponement, without patience, and without the slightest regard for the physical realities or social consequences of the external world.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "When a child enters this world, it is at first nothing other than pure, undiluted Id. When an infant is cold, frightened, or hungry, it screams with raw, unconstrained fury. It has no conception of its mother's exhaustion, no patience for societal decorum, and no understanding of delay. It demands satisfaction now, absolute and complete."}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'We naively assume that as we mature into responsible, dignified adults, we leave this primitive animal behind in the nursery. But psychoanalysis reveals that the Id never grows up. It never acquires a conscience, it never learns restraint, and it never ceases to hunger for primal dominance and immediate sensual discharge.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'The civilized human being merely covers this raging cauldron with a delicate veneer of manners, philosophy, and professional duty. Yet every night, when the conscious sentinels of the mind lower their guard during sleep, the Id reawakens, expressing its raw, uninhibited libido through the distorted symbols and bizarre dramas of our dream life.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'If humanity were governed solely by the primitive passions of the Id, our civilization would instantly collapse into an apocalyptic nightmare of murder, plunder, and unrestricted sensual indulgence. Nature and survival demand that a protective barrier be formed between this seething beast and the outer world.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "Out of this urgent biological necessity arises the second agency of the human mind: the Ego, or das Ich — the 'I'. The Ego is that specialized, highly developed portion of the Id which has been modified and molded by direct, continuous contact with the external physical reality through perception."}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'While the Id operates under the impulsive Pleasure Principle, the Ego institutes what Freud called the Reality Principle. The Ego does not abandon the search for pleasure; rather, it introduces caution, planning, memory, and delay. It evaluates the physical environment to discover safe, socially viable pathways to discharge instinctual tension without courting catastrophe.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "Freud offered an unforgettable and masterly analogy to capture this delicate dynamic: 'The Ego is like a man on horseback, who has to hold in check the superior strength of the horse; with this difference, that the rider tries to do so with his own strength, while the Ego uses borrowed forces.'"}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "And Freud noted with profound irony: 'Often a rider, if he is not to be parted from his horse, is obliged to guide it where it wants to go; so in the same way the Ego is in the habit of transforming the Id's will into action as if it were its own.' Much of what we proudly call our conscious, rational decision-making is merely our Ego inventing clever excuses for our Id's demands."}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Consider the tragic and exhausting burden carried by the human Ego. Freud described the Ego as a poor creature serving three tyrannical masters at the exact same moment: the rigid, unforgiving realities of the external world; the voracious, violent demands of the Id; and the savage, hyper-moral cruelty of the Superego.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Whenever the Ego finds itself stretched beyond its capacity to mediate between these warring masters, it is struck by that universal psychological distress signal: anxiety, or Angst. Realist anxiety before the tangible perils of survival; neurotic anxiety before the terrifying eruptions of the Id; and moral anxiety before the condemnation of conscience.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'To preserve its sanity and prevent total nervous collapse under this intense psychological warfare, the Ego develops an arsenal of unconscious defense mechanisms: repression, projection, displacement, reaction formation, and rationalization. These defenses are psychological levies thrown up against the flooding waters of inner chaos.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Yet these defenses exact a catastrophic emotional tax. For whatever truth the Ego represses into the unconscious does not quietly perish. Denied conscious expression, it festers in the dark, mutating into debilitating panic attacks, psychosomatic illnesses, paralyzing phobias, and repetitive self-sabotage.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "We arrive now at the third and most formidable structure in Freud's architecture: the Superego, or das Über-Ich — the 'Over-I'. What is human conscience? Is our moral compass a divine light implanted in our souls, or is it a psychological artifact forged in the fires of childhood development?"}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "Freud discovered that the Superego is the internalized residue of early parental authority and cultural conditioning. During early childhood, the helpless child dreads the loss of its parents' love and the terror of physical punishment. In navigating the forbidden desires and rivalries of the Oedipal phase, the child resolves the crisis by introjecting the forbidding father into the core of his own psyche."}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "The external father who once said 'Thou shalt not' is transformed into an internal prosecutor that watches the Ego with unblinking, omniscient vigilance. The Superego constructs two distinct pillars: the Conscience, which punishes with guilt, and the Ego Ideal, an impossibly lofty standard of perfection against which the Ego is perpetually measured and found wanting."}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Here lies the terrifying and sadistic nature of the Superego: unlike human courts of law, which can only punish outward actions that have physically occurred, the Superego punishes the Ego for mere unconscious thoughts, fleeting fantasies, and unacted desires. You can conceal a crime from the world, but you cannot conceal a passing thought from your Superego.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'The very moment an illicit desire or aggressive impulse stirs in the subterranean waters of the Id, the Superego detects the tremor. It retaliates immediately, drowning the helpless Ego in suffocating waves of mysterious guilt, unworthiness, chronic anxiety, and self-disgust.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'This explains one of the most astonishing paradoxes of human psychology: why is it that the most virtuous, honest, and saintly individuals often suffer from the most agonizing feelings of moral failure and unworthiness, while the hardened sociopath walks through life with a cheerful, untroubled conscience?'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'The criminal has an underdeveloped, feeble Superego that demands little of him. But the conscientious, noble soul, by constantly suppressing his instincts and demanding moral purity, diverts the unused aggressive energy of his Id directly into his Superego, weaponizing his conscience into a vicious internal executioner.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'In severe melancholia and pathological depression, this internal executioner turns upon the Ego with demonic ferocity. It berates the self as worthless, sinful, and deserving of destruction. Freud demonstrated that suicide is often the tragic climax of this internal trial, where a hyper-moral Superego murders the very self it was designed to protect.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'To look deeply into this internal battlefield is to understand why modern human beings are perpetually exhausted, anxious, and at war with themselves. We are not simple, unified creatures; we are walking coalitions of conflicting impulses, biological drives, and punitive moral taboos.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'What, then, is the grand therapeutic purpose of psychoanalysis? Freud was never an idle optimist or a romantic dreamer. He famously remarked that the ultimate purpose of analysis is merely to transform hysterical misery into common human unhappiness — that is, into an honest, sober, and unvarnished relationship with reality.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "Yet he provided humanity with one of the most inspiring and heroic ethical declarations ever formulated in the history of psychology: 'Wo Es war, soll Ich werden' — 'Where Id was, there Ego shall be.' It is a monumental work of cultural reclamation, like the draining of the Zuyder Zee in the Netherlands."}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'To reclaim the fertile land from the turbulent ocean of the unconscious does not mean waging a futile war of extermination against our biological instincts. That is the tragic, naive blunder of moral fanaticism and puritanical repression, which succeeds only in driving desires into darkness where they turn toxic.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Rather, it requires the supreme psychological courage of self-honesty. You must cultivate the intellectual bravery to descend into your own depths, to look directly into the fierce appetites and selfish longings of your Id, without flinching and without hypocritical condemnation.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "When you bring the light of conscious awareness to your buried desires, you disarm their subterranean tyranny. You cease to be the helpless puppet of unresolved childhood wounds. You stop calling your self-inflicted patterns of destruction 'fate' when they are merely your own unacknowledged drives operating in the dark."}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Simultaneously, you must learn to stand firm against the tyrannical, irrational demands of your Superego. You must learn to distinguish between genuine, compassionate empathy that makes human society possible, and the neurotic, self-punishing perfectionism that drains your vitality and paralyzes your soul.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'This leads to the highest summit of human psychological maturity: the sacred art of Sublimation. Sublimation is the miraculous mental capacity to take the raw, primitive, sexual and aggressive energy of the Id, and instead of repressing it, divert its tremendous currents into the creation of monumental art, scientific breakthrough, philosophical wisdom, and enduring devotion.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'You do not achieve peace by denying that you are an animal; nor do you achieve dignity by pretending you are an angel. True sovereignty is found in strengthening the conscious Ego: standing squarely in the storm, honoring your passions, governing them with reason, and sculpting your instincts into an enduring work of cultural beauty.'}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': "In the immortal, contemplative words of Sigmund Freud: 'One day, in retrospect, the years of struggle will strike you as the most beautiful.'"}, {'speaker': 'male', 'name': 'The Psychoanalyst', 'text': 'Thank you for descending with us into The Freudian Depths. If this psychoanalytic exploration of the Id, Ego, and Superego has illuminated the quiet corridors of your own soul, subscribe to our channel, share your reflections in the comments below, and walk forward with unbroken intellectual courage. Until our next descent — know thyself.'}]

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

# --- Robust AI dialogue generation (chunked, truncation-proof) ---
TARGET_TURNS = 40
TURNS_PER_ACT = (TARGET_TURNS + 4) // 5
MAX_ACT_ATTEMPTS = 4
MIN_TURNS = 30
MIN_WORDS = 1500
NARRATOR_NAME = "The Psychoanalyst"
NARRATOR_SPEAKER = "male"
NARRATOR_PERSONA = "Sigmund Freud's intellectual heir and the lead psychoanalyst for 'The Freudian Depths' channel. Deep, clinical, aristocratic psychoanalytic narration in the contemplative cadence of Sigmund Freud"


def normalize_turn_text(text):
    """Normalize turn text for duplicate detection."""
    return re.sub(r'[^a-z0-9\s]', '', (text or '').lower()).strip()


def dialogue_fingerprint(dialogue):
    """Stable hash of a dialogue's normalized texts (order-independent)."""
    norm = sorted(normalize_turn_text(t.get('text', '')) for t in dialogue or [])
    norm = [t for t in norm if t]
    return hashlib.sha256('\n'.join(norm).encode('utf-8')).hexdigest()


def load_history_hashes():
    """Load dialogue fingerprints of previously published episodes."""
    hashes = set()
    for fname in ["published_videos.json", "history.json"]:
        fpath = os.path.join(config.BASE_DIR, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and item.get("dialogue_hash"):
                                hashes.add(item["dialogue_hash"])
            except Exception:
                pass
    return hashes


def repair_and_extract_turns(content, speaker="male", name=None):
    """Extract valid dialogue turns from possibly-truncated AI JSON.

    Salvages every complete turn object even when the response was cut off
    mid-stream, so truncated calls still contribute usable turns.
    """
    name = name or NARRATOR_NAME
    turns = []
    if not content:
        return turns
    text = content.strip()
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()
    candidates = []
    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and isinstance(obj.get("dialogue"), list):
            candidates = obj["dialogue"]
        elif isinstance(obj, list):
            candidates = obj
    except Exception:
        obj = None
    if not candidates:
        for m in re.finditer(r'\{[^{}]*"text"\s*:\s*"(?:[^"\\]|\\.)*"[^{}]*\}', text):
            try:
                candidates.append(json.loads(m.group(0)))
            except Exception:
                continue
    for c in candidates:
        if not isinstance(c, dict):
            continue
        t = (c.get("text") or "").strip()
        if not t:
            continue
        turns.append({
            "speaker": c.get("speaker") or speaker,
            "name": c.get("name") or name,
            "text": t,
        })
    return turns


def _pollinations_endpoint():
    return getattr(config, "POLLINATIONS_ENDPOINT", None) or "https://text.pollinations.ai/"


def _pollinations_model():
    return getattr(config, "POLLINATIONS_MODEL", None) or "openai"


def request_dialogue_chunk(act_title, act_summary, topic, ep_num, need, tail_texts, attempt, past_topics=None):
    """One small AI call for a few turns of a single act. Raises on failure."""
    endpoint = _pollinations_endpoint()
    model = _pollinations_model()
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("POLLINATIONS_API_KEY") or getattr(config, "POLLINATIONS_API_KEY", "")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    continuity = ""
    if tail_texts:
        continuity = ("Story so far (continue seamlessly, do not repeat these ideas):\n"
                      + "\n".join(f"- {t[:220]}" for t in tail_texts[-2:]) + "\n")
    avoid = ""
    if past_topics:
        avoid = f"Do not cover these already-published topics: {'; '.join(past_topics[:12])}.\n"
    prompt = f"""You are {NARRATOR_PERSONA}.
Write EXACTLY {need} consecutive dialogue turns for Episode #{ep_num} about "{topic}".
Current act: {act_title} - {act_summary}.
{continuity}{avoid}RULES:
1. Single narrator named "{NARRATOR_NAME}" (speaker "male").
2. Each turn 60-100 words of rich, substantive narration, fresh ideas only, no repetition within or across turns.
3. Return ONLY a JSON array: [{{"speaker": "male", "name": "{NARRATOR_NAME}", "text": "..."}}]"""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": round(min(1.1, 0.85 + 0.05 * attempt), 2),
        "max_tokens": 2500,
    }
    r = requests.post(endpoint, json=payload, headers=headers, timeout=90)
    if r.status_code != 200:
        raise RuntimeError(f"AI HTTP {r.status_code}: {(r.text or '')[:200]}")
    data = r.json()
    if isinstance(data, dict) and data.get("choices"):
        content = data["choices"][0]["message"]["content"]
        turns = repair_and_extract_turns(content)
        if not turns:
            raise RuntimeError("AI returned no usable dialogue turns")
        return turns
    if isinstance(data, dict) and isinstance(data.get("dialogue"), list):
        turns = repair_and_extract_turns(json.dumps(data["dialogue"]))
        if turns:
            return turns
        raise RuntimeError("AI returned no usable dialogue turns")
    if isinstance(data, list):
        turns = repair_and_extract_turns(json.dumps(data))
        if turns:
            return turns
        raise RuntimeError("AI returned no usable dialogue turns")
    raise RuntimeError("AI returned an unrecognized response shape")


def generate_dynamic_story_ai(topic=None, ep_num=1, past_topics=None, acts=None, target_turns=None):
    """Builds original dialogue act-by-act with retries. Raises instead of
    silently reusing a previous episode's script."""
    if past_topics is None:
        past_topics = load_history_topics()
    if not acts:
        acts = [("Full Episode", topic or "")]
    if not target_turns:
        target_turns = TARGET_TURNS
    per_act = max(2, (target_turns + len(acts) - 1) // len(acts))
    dialogue = []
    seen = set()
    for act_idx, act in enumerate(acts):
        act_title = act[0] if isinstance(act, (list, tuple)) else str(act)
        act_summary = act[1] if isinstance(act, (list, tuple)) and len(act) > 1 else ""
        collected = 0
        for attempt in range(MAX_ACT_ATTEMPTS):
            try:
                tail = [t["text"] for t in dialogue[-2:]]
                chunk = request_dialogue_chunk(
                    act_title, act_summary, topic, ep_num, per_act, tail,
                    attempt + act_idx, past_topics)
                fresh = 0
                for t in chunk:
                    norm = normalize_turn_text(t.get("text", ""))
                    if norm and norm not in seen and len(t.get("text", "").split()) >= 5:
                        seen.add(norm)
                        dialogue.append(t)
                        fresh += 1
                        collected += 1
                        if collected >= per_act:
                            break
                print(f"[StoryGenerator] Act {act_idx + 1}/{len(acts)} attempt {attempt + 1}: +{fresh} turns "
                      f"(total {len(dialogue)}/{target_turns})")
                if collected >= per_act:
                    break
            except Exception as e:
                print(f"[StoryGenerator] Act {act_idx + 1}/{len(acts)} attempt {attempt + 1} issue: {e}")
                time.sleep(2)
        if collected < max(2, per_act - 2):
            raise RuntimeError(
                f"AI dialogue generation failed for act {act_idx + 1} ('{act_title}') after "
                f"{MAX_ACT_ATTEMPTS} attempts. Aborting instead of publishing a repeat.")
    return {"topic": topic, "focus": "", "dialogue": dialogue}

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
    if catalog_item["id"] == "ep_1":
        dialogue = EPISODE_1_SCRIPT
    else:
        ai_story = generate_dynamic_story_ai(
            topic=catalog_item["topic"],
            ep_num=ep_num,
            past_topics=past_topics,
            acts=catalog_item["acts"],
            target_turns=TARGET_TURNS,
        )
        dialogue = ai_story["dialogue"]

    total_script_words = sum(len((t.get("text") or "").split()) for t in dialogue or [])
    if not dialogue or len(dialogue) < MIN_TURNS or total_script_words < MIN_WORDS:
        raise RuntimeError(
            f"AI dialogue generation produced only {len(dialogue or [])} turns / {total_script_words} words "
            f"(minimum {MIN_TURNS} turns / {MIN_WORDS} words). Aborting instead of publishing a repeat.")

    dialogue_hash = dialogue_fingerprint(dialogue)
    if dialogue_hash in load_history_hashes():
        raise RuntimeError("Generated dialogue duplicates a previously published episode. Aborting instead of publishing a repeat.")

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
        "dialogue": dialogue,
        "dialogue_hash": dialogue_hash
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
