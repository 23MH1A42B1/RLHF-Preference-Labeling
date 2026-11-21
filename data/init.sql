-- RLHF Preference Tool Database Initialization
CREATE TABLE IF NOT EXISTS labels (
    id SERIAL PRIMARY KEY,
    prompt TEXT NOT NULL,
    response_a TEXT NOT NULL,
    response_b TEXT NOT NULL,
    category VARCHAR(255) NOT NULL,
    annotator_id VARCHAR(255),
    chosen VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    labeled_at TIMESTAMP WITH TIME ZONE,
    pair_id INTEGER
);

CREATE INDEX IF NOT EXISTS idx_labels_annotator_id ON labels(annotator_id);
CREATE INDEX IF NOT EXISTS idx_labels_category ON labels(category);
CREATE INDEX IF NOT EXISTS idx_labels_pair_id ON labels(pair_id);

INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (1, 'What is the capital of France?', 'The capital of France is Paris, located in the north-central part of the country along the Seine River.', 'France''s capital city is Lyon, famous for its gastronomy and silk production.', 'factual_qa', NULL, NULL, NOW(), 1) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (2, 'How does photosynthesis work in plants?', 'Photosynthesis is the process by which green plants and certain organisms transform light energy into chemical energy. During photosynthesis, light energy is captured by chlorophyll and used to convert water, carbon dioxide, and minerals into oxygen and energy-rich organic compounds like glucose.', 'Photosynthesis is when plants absorb oxygen from the soil at night and turn it into nitrogen using heat from the ground.', 'factual_qa', NULL, NULL, NOW(), 2) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (3, 'What causes ocean tides on Earth?', 'Tides are primarily caused by the gravitational pull of the Moon and the Sun on Earth''s oceans, combined with the rotation of the Earth.', 'Ocean tides are driven exclusively by undersea seismic activity and warm ocean currents pushing water toward coastlines.', 'factual_qa', NULL, NULL, NOW(), 3) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (4, 'Who developed the theory of general relativity?', 'Albert Einstein developed the theory of general relativity, publishing it in 1915.', 'Sir Isaac Newton formulated general relativity in 1687 in his famous work Philosophiae Naturalis Principia Mathematica.', 'factual_qa', NULL, NULL, NOW(), 4) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (5, 'What is the boiling point of water at sea level in Celsius and Fahrenheit?', 'At standard atmospheric pressure at sea level, water boils at 100°C (212°F).', 'Water boils at 90°C or approximately 194°F at sea level.', 'factual_qa', NULL, NULL, NOW(), 5) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (6, 'Which planet in our solar system has the highest number of recognized moons?', 'Saturn holds the record for the most recognized moons in our solar system, with 146 confirmed moons.', 'Mars has the most moons because of its proximity to the asteroid belt.', 'factual_qa', NULL, NULL, NOW(), 6) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (7, 'What is the primary function of red blood cells in the human body?', 'Red blood cells (erythrocytes) transport oxygen from the lungs to body tissues and bring carbon dioxide back to the lungs to be exhaled.', 'Red blood cells are primarily responsible for producing antibodies and attacking bacterial infections.', 'factual_qa', NULL, NULL, NOW(), 7) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (8, 'When was the United Nations established?', 'The United Nations was established on October 24, 1945, following World War II, with the ratification of the UN Charter.', 'The United Nations was founded in 1919 immediately after the Treaty of Versailles.', 'factual_qa', NULL, NULL, NOW(), 8) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (9, 'What is the chemical symbol for gold, and what Latin word does it originate from?', 'The chemical symbol for gold is Au, derived from the Latin word ''aurum'', meaning shining dawn.', 'The symbol for gold is Gd, which comes from the Latin word ''gildus''.', 'factual_qa', NULL, NULL, NOW(), 9) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (10, 'Which mountain is the highest peak in North America?', 'Denali (formerly known as Mount McKinley) in Alaska is the highest peak in North America, with a summit elevation of 20,310 feet (6,190 meters).', 'Mount Whitney in California is the tallest peak in North America at 14,505 feet.', 'factual_qa', NULL, NULL, NOW(), 10) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (11, 'What is the speed of light in a vacuum?', 'The speed of light in a vacuum is approximately 299,792,458 meters per second (roughly 300,000 km/s or 186,282 miles per second).', 'The speed of light in a vacuum is roughly 150,000 meters per second.', 'factual_qa', NULL, NULL, NOW(), 11) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (12, 'What is the largest living species of mammal currently known?', 'The blue whale (Balaenoptera musculus) is the largest mammal—and the largest animal—known to have ever existed.', 'The African bush elephant is the largest living mammal on Earth.', 'factual_qa', NULL, NULL, NOW(), 12) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (13, 'Write a Python function to check whether a string is a palindrome, ignoring spaces, punctuation, and capitalization.', 'import re

def is_palindrome(text: str) -> bool:
    cleaned = re.sub(r''[^a-zA-Z0-9]'', '''', text).lower()
    return cleaned == cleaned[::-1]', 'def is_palindrome(text):
    return text == reversed(text)', 'code_generation', NULL, NULL, NOW(), 13) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (14, 'Write a JavaScript function that debounces a given callback function by a specified delay.', 'function debounce(func, delayMs) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delayMs);
  };
}', 'function debounce(func, delayMs) {
  setTimeout(func, delayMs);
}', 'code_generation', NULL, NULL, NOW(), 14) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (15, 'Write a SQL query to find the second highest salary from an Employee table.', 'SELECT MAX(salary) AS SecondHighestSalary 
FROM Employee 
WHERE salary < (SELECT MAX(salary) FROM Employee);', 'SELECT salary FROM Employee ORDER BY salary DESC LIMIT 2;', 'code_generation', NULL, NULL, NOW(), 15) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (16, 'Write a Python function to flatten a deeply nested list of arbitrary depth.', 'def flatten_list(nested):
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat', 'def flatten_list(nested):
    return [item for sublist in nested for item in sublist]', 'code_generation', NULL, NULL, NOW(), 16) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (17, 'Write a TypeScript interface and generic function for a standard Result type with Ok and Err variants.', 'type Result<T, E> = 
  | { ok: true; value: T }
  | { ok: false; error: E };

function Ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}', 'function Result(val) {
  if (val) return true;
  return false;
}', 'code_generation', NULL, NULL, NOW(), 17) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (18, 'Write a Python context manager that measures and prints the execution time of a code block.', 'import time
from contextlib import contextmanager

@contextmanager
def timer(label: str = ''Execution''):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f''{label} took {elapsed:.4f} seconds'')', 'def timer():
    t1 = time.time()
    return time.time() - t1', 'code_generation', NULL, NULL, NOW(), 18) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (19, 'Write a React hook `useLocalStorage` to persist and synchronize state with window.localStorage.', 'import { useState, useEffect } from ''react'';

export function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (err) {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (err) {
      console.error(err);
    }
  }, [key, value]);

  return [value, setValue];
}', 'function useLocalStorage(key) {
  return localStorage.getItem(key);
}', 'code_generation', NULL, NULL, NOW(), 19) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (20, 'Implement binary search in Python returning the index of the target or -1 if not found.', 'def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1', 'def binary_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1', 'code_generation', NULL, NULL, NOW(), 20) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (21, 'Write a bash one-liner to find all .log files in /var/log modified in the last 24 hours and compress them.', 'find /var/log -name ''*.log'' -type f -mtime -1 -exec gzip {} +', 'tar -czf logs.tar.gz /var/log/*.log', 'code_generation', NULL, NULL, NOW(), 21) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (22, 'Write a Python function to parse an ISO 8601 date string and return a UTC datetime object.', 'from datetime import datetime, timezone

def parse_iso(iso_str: str) -> datetime:
    dt = datetime.fromisoformat(iso_str)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)', 'import datetime
def parse_iso(s):
    return datetime.datetime.strptime(s, ''%Y-%m-%d'')', 'code_generation', NULL, NULL, NOW(), 22) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (23, 'Write a Dockerfile for a lightweight Node.js Express microservice.', 'FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
USER node
CMD ["node", "index.js"]', 'FROM ubuntu
RUN apt-get update && apt-get install -y nodejs
COPY . .
CMD node app.js', 'code_generation', NULL, NULL, NOW(), 23) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (24, 'Write a Python decorator that retries a function up to max_retries times upon catching an exception.', 'import time
from functools import wraps

def retry(max_retries=3, delay=1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator', 'def retry(func):
    try:
        return func()
    except:
        return func()', 'code_generation', NULL, NULL, NOW(), 24) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (25, 'Write a short poem about an old clockmaker who repairs an antique pocket watch that seems to bend time.', 'With trembling hands and loupe to eye,
He coaxed the rusted gears to sigh.
Each jewel aligned, each pivot spun,
Until the brass reversed the sun.
A tick leapt back, a second stayed,
In shadows where the moonlight played;
He wound the spring, turned back the year,
And felt his lost youth drawing near.', 'There once was a clockmaker old,
Whose pocket watch was made of gold.
He fixed up the gear,
And drank down a beer,
Now time does whatever it''s told.', 'creative_writing', NULL, NULL, NOW(), 25) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (26, 'Describe a bustling sci-fi night market situated inside the hollowed-out shell of an ancient asteroid.', 'Neon filaments crisscrossed the jagged cavern ceiling of Vesta-9, casting iridescent violet shadows over crowded catwalks. Steam hissed from noodle carts serving synth-kelp broth, while holographic hawkers shouted prices in a dozen planetary dialects. Miners in grease-stained magnetic boots haggled over hydro-cells and unrefined quartz, their laughter muffled by the gentle hum of artificial gravity generators anchored deep within the iron bedrock.', 'It was a market in space. There were stalls selling alien fruits and gadgets. People walked around and bought things under dim lights. It was very noisy and full of aliens.', 'creative_writing', NULL, NULL, NOW(), 26) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (27, 'Write an opening paragraph for a noir detective mystery set in a perpetual rainstorm in Seattle.', 'Rain in Seattle doesn''t wash away sins; it just marinates them. It drummed a relentless cadence against my frosted office window, blurring the neon sign across 4th Avenue into a bleeding crimson smear. When she walked in, smelling of expensive tobacco and cheap alibis, water dripped from her trench coat onto my linoleum like pennies falling into an empty wishing well.', 'I sat in my Seattle office. It was raining hard outside, like it always does. The door opened and a tall lady walked in looking for help with a stolen necklace. I took a sip of my coffee.', 'creative_writing', NULL, NULL, NOW(), 27) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (28, 'Write a dialogue between an immortal wanderer and a mortal tavern keeper about the bittersweet nature of time.', '''Another flagon, traveler?'' the keeper asked, wiping the worn oak counter. ''You look at the hearth like you’ve seen empires turn to ash.''

''I have, my friend,'' the wanderer replied softly, fingers tracing the grain of the wood. ''The curse is not remembering the kings or monuments—it is remembering the laughter of friends whose names the wind forgot three thousand winters ago. You measure your life in harvests; I measure mine in grief.''

The keeper paused, setting down the mug. ''Perhaps. But tomorrow morning, my bread will still be warm, and that is enough.''', '''Hey, you are old right?'' the tavern keeper said.
''Yeah, I live forever,'' said the immortal.
''Must be cool!''
''No, everyone I know dies and it gets boring after a while,'' the immortal sighed.', 'creative_writing', NULL, NULL, NOW(), 28) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (29, 'Compose a lyrical description of an abandoned library overgrown by a primeval forest.', 'Ivy cascaded across ruined marble arches like emerald curtains, framing aisles where towering oaks had shattered the flagstones. Moldering leather tomes lay open in dappled sunlight, their parchment pages transformed into nurseries for delicate maidenhair ferns. Where scholars once whispered over forgotten philosophies, birds now nested among cracked stone corbels, singing to books that only the wind cared to read.', 'The old library was broken down and trees grew inside it. Grass covered the floor and books were rotten on the shelves. Birds were flying around the broken roof.', 'creative_writing', NULL, NULL, NOW(), 29) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (30, 'Write a motivational opening speech for a rookie astronaut stepping onto the surface of Mars for the first time.', '''To everyone listening two hundred million miles away: we left Earth not to escape our home, but to prove what human courage can build across the dark. As our boots touch this crimson dust, we carry the hopes of every dreamer who ever looked up at the night sky. This is not just a footprint on Mars; it is humanity''s promise that our journey is only beginning.''', '''Okay guys, we are finally on Mars. It''s very red and dusty out here. Let''s make sure we do all our experiments and don''t trip over the rocks. Good job everyone.''', 'creative_writing', NULL, NULL, NOW(), 30) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (31, 'Write a short fairy-tale opening about a tailor who spins cloaks from stolen moonlight.', 'At the edge of the Whispering Woods lived Barnaby, a tailor whose needle was carved from thistle-bone and whose thread was spun from moonbeams reaped on cloudless midnight skies. The cloaks he fashioned were as cool as well water and weightless as breath, conferring quiet invisibility to those whose hearts carried no malice.', 'Once upon a time there was a tailor named Bob. Every full moon he caught moonlight with a jar and made coats out of it that made people invisible. He sold them for gold.', 'creative_writing', NULL, NULL, NOW(), 31) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (32, 'Write a flash fiction piece about two satellites having a farewell conversation before de-orbiting into the Pacific Ocean.', '''Telemetry confirms entry vector in three minutes, Astra-4,'' Pioneer-7 radioed across the silent thermosphere. ''Did we transmit enough?''

Astra-4 adjusted its solar array toward the sun one final time. ''We watched hurricanes cradle continents and charted ten billion stars for children who will never know our names. That is enough, old friend. See you in the fire.''', '''I am about to fall down to Earth,'' said Astra-4.
''Me too,'' replied Pioneer-7. ''It was nice working with you.''
''Yes, goodbye now,'' Astra said as they crashed.', 'creative_writing', NULL, NULL, NOW(), 32) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (33, 'Write a monologue from the perspective of an old lighthouse keeper preparing for a storm of the century.', '''Let the black waves rise; this tower was wedded to bedrock before my grandfather took his first breath. Check the oil reservoirs, trim the wick, grease the brass gimbals. Ships out on the shoal have nothing between them and the jagged reef but eighty thousand candles of white light. As long as air fills my lungs, that beacon will not flicker.''', '''Big storm coming tonight. Hope the lighthouse glass doesn''t break. I put extra oil in the lamp and closed the windows. Better go make some tea.''', 'creative_writing', NULL, NULL, NOW(), 33) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (34, 'Describe the sensation of waking up from a 300-year cryogenic sleep on an interstellar colony ship.', 'Consciousness returned not as a spark, but as a frostbitten tremor deep inside my bones. The amniotic gel drained with a muted hiss, leaving skin stinging in the sterilized chill of Bay C. Needles retracted from numb arteries, and when my eyelids pried apart, the amber glow of the diagnostic terminal flickered with a single message: ''Year 2341. Welcome to Epsilon Eridani.''', 'I opened my eyes and was very cold. The glass tube opened and fluid poured out on the floor. A robot voice said three hundred years had passed and we were near a new planet.', 'creative_writing', NULL, NULL, NOW(), 34) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (35, 'Write a micro-story about a forgotten god who survives by taking care of stray cats in an alley.', 'Centuries ago, thousands knelt before his marble altars praying for thunder. Now, in the damp alley behind Anton''s bakery, the old storm god warmed saucers of cream with the gentle static of his fingertips. A three-legged tabby purred against his worn sandal, and he smiled—finding more devotion in a single feline headbutt than in a kingdom''s gilded hymns.', 'A god who used to have temples now lives in an alleyway. People don''t pray to him anymore so he feeds leftover fish to stray cats so he doesn''t feel lonely.', 'creative_writing', NULL, NULL, NOW(), 35) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (36, 'Write an evocative paragraph describing autumn arriving in a mountain village.', 'Autumn slipped into the high valley on a crisp north wind, setting the aspen groves ablaze in shimmering amber and copper. Woodsmoke curled from stone chimneys to mingle with the tang of fallen pine needles, while villagers hurried to stack split birch against shed walls before the first frost claimed the pumpkin patches.', 'Autumn came to the village. The leaves changed colors to red and yellow and fell off the trees. People made fires because it was getting colder outside.', 'creative_writing', NULL, NULL, NOW(), 36) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (37, 'Summarize the primary purpose and key benefits of the Git version control system.', 'Git is a distributed version control system designed to track changes in source code during software development. Its key benefits include robust history tracking, seamless branching and merging, decentralized collaboration without relying on a single central server, and cryptographic integrity of commit histories.', 'Git is an online cloud platform where people put their code files to share with friends on social media.', 'summarization', NULL, NULL, NOW(), 37) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (38, 'Summarize the core mechanism of action of mRNA vaccines.', 'mRNA vaccines deliver synthetic messenger RNA instructions into host cells, prompting them to temporarily produce a harmless viral antigen (such as the spike protein). The immune system recognizes this foreign antigen, develops targeted antibodies, and establishes memory T and B cells without exposing the body to the live virus.', 'mRNA vaccines inject dead virus particles directly into the bloodstream to kill infections.', 'summarization', NULL, NULL, NOW(), 38) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (39, 'Summarize the key events and historical significance of the Magna Carta signed in 1215.', 'In June 1215 at Runnymede, English barons compelled King John to sign the Magna Carta. By asserting that the monarch was subject to the law and guaranteeing rights like due process and protection from unlawful imprisonment, it established foundational principles that influenced modern constitutional law and civil liberties.', 'The Magna Carta was a peace treaty between England and France that ended the Hundred Years War.', 'summarization', NULL, NULL, NOW(), 39) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (40, 'Summarize the greenhouse effect and how human activities intensify it.', 'The greenhouse effect is a natural process where atmospheric gases (like CO2, methane, and water vapor) trap thermal radiation emitted by Earth''s surface, keeping the planet habitable. Human activities—principally burning fossil fuels and deforestation—increase greenhouse gas concentrations, amplifying heat retention and driving anthropogenic climate change.', 'The greenhouse effect means farmers build glass greenhouses that reflect sunlight away into outer space.', 'summarization', NULL, NULL, NOW(), 40) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (41, 'Summarize the architectural differences between Monolithic and Microservices architectures.', 'Monolithic architecture packages all application components, business logic, and databases into a single unified codebase and deployment unit, simplifying initial development but hindering independent scaling. In contrast, microservices decouple functionality into small, autonomous services communicating over APIs, enabling independent deployments, distinct tech stacks, and resilient scalability at the cost of operational complexity.', 'Monoliths are written in C++ while microservices are only written in JavaScript.', 'summarization', NULL, NULL, NOW(), 41) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (42, 'Summarize the concept and trade-offs of the CAP theorem in distributed computing.', 'The CAP theorem states that a distributed data store can guarantee at most two of three properties simultaneously: Consistency (all nodes see the exact same data simultaneously), Availability (every request receives a non-error response), and Partition Tolerance (the system continues operating despite network packet loss). In practice, because network partitions are unavoidable, systems must choose between Consistency (CP) and Availability (AP).', 'The CAP theorem says computers can only do caching, authentication, and processing.', 'summarization', NULL, NULL, NOW(), 42) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (43, 'Summarize the fundamental principles of the Agile software development methodology.', 'Agile emphasizes iterative delivery, customer collaboration, cross-functional self-organizing teams, and adaptability to changing requirements over rigid upfront planning and extensive documentation. Work is divided into short sprints that yield functional, tested increments of software.', 'Agile means developers write code as fast as possible without writing any unit tests or specifications.', 'summarization', NULL, NULL, NOW(), 43) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (44, 'Summarize the economic concept of Supply and Demand and how it determines equilibrium price.', 'The law of supply and demand posits that higher prices incentivize producers to supply more goods while discouraging consumer demand, and vice-versa. Market equilibrium is reached at the price point where the quantity demanded by consumers precisely equals the quantity supplied by producers.', 'Supply and demand is when the government fixes all prices in stores once every quarter.', 'summarization', NULL, NULL, NOW(), 44) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (45, 'Summarize the role of mitochondria in eukaryotic cells.', 'Mitochondria are membrane-bound organelles commonly known as the cellular powerhouses. They generate the bulk of cellular adenosine triphosphate (ATP) through oxidative phosphorylation and the Krebs cycle, while also regulating cellular metabolism, calcium signaling, and apoptosis.', 'Mitochondria hold the cell''s genetic code in chromosomes and organize protein synthesis on ribosomes.', 'summarization', NULL, NULL, NOW(), 45) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (46, 'Summarize the main principles of Object-Oriented Programming (OOP).', 'The four pillars of OOP are: Encapsulation (bundling data and methods while restricting direct access), Abstraction (hiding implementation complexity behind clear interfaces), Inheritance (enabling classes to inherit properties and behaviors from parent classes), and Polymorphism (allowing distinct objects to respond to the same interface in specific ways).', 'OOP means using global variables, recursive functions, and goto statements to write fast programs.', 'summarization', NULL, NULL, NOW(), 46) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (47, 'Summarize how public-key (asymmetric) cryptography works.', 'Asymmetric cryptography utilizes mathematically linked key pairs: a public key for encryption and a private key kept secret for decryption (or signing). Data encrypted with the public key can only be decrypted by the corresponding private key, ensuring secure communication across untrusted networks without prior shared secrets.', 'Asymmetric cryptography means the sender and receiver both memorize the exact same secret password.', 'summarization', NULL, NULL, NOW(), 47) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (48, 'Summarize the causes and consequences of the 2008 global financial crisis.', 'The 2008 financial crisis was sparked by the collapse of the US subprime mortgage market, exacerbated by excessive financial deregulation, predatory lending, and complex mortgage-backed derivatives. It led to major investment bank failures (such as Lehman Brothers), severe global credit freezes, stock market crashes, and the Great Recession.', 'The 2008 crisis was caused by a sudden global shortage of physical cash printed by central banks.', 'summarization', NULL, NULL, NOW(), 48) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (49, 'If all roses are flowers and some flowers fade quickly, can we logically conclude that some roses fade quickly?', 'No, we cannot logically conclude that. While all roses are flowers, the subset of flowers that fade quickly might not overlap with the subset of flowers that are roses. It is possible that only non-rose flowers fade quickly.', 'Yes, because roses are flowers and some flowers fade quickly, roses must be among those that fade quickly.', 'reasoning', NULL, NULL, NOW(), 49) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (50, 'A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?', 'The ball costs $0.05 (5 cents). Let ball = x. Then bat = x + 1.00. Total = x + (x + 1.00) = 2x + 1.00 = 1.10. Solving gives 2x = 0.10, so x = $0.05. The bat costs $1.05.', 'The ball costs $0.10, because $1.10 minus $1.00 is $0.10.', 'reasoning', NULL, NULL, NOW(), 50) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (51, 'If five machines take five minutes to make five widgets, how long would it take 100 machines to make 100 widgets?', 'It would take 5 minutes. If five machines make five widgets in five minutes, then each machine makes one widget in five minutes. Therefore, 100 machines working in parallel will each make one widget in five minutes, yielding 100 widgets total.', 'It would take 100 minutes, because 100 machines making 100 widgets scales proportionally.', 'reasoning', NULL, NULL, NOW(), 51) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (52, 'You have a 3-liter jug and a 5-liter jug, and an unlimited supply of water. How can you measure exactly 4 liters?', '1. Fill the 5L jug completely.
2. Pour water from the 5L jug into the 3L jug until full (leaving 2L in the 5L jug).
3. Empty the 3L jug.
4. Pour the 2L from the 5L jug into the 3L jug.
5. Fill the 5L jug completely again.
6. Pour water from the 5L jug into the 3L jug until full (it only needs 1L, since it already holds 2L).
7. The 5L jug now contains exactly 4 liters.', 'Fill both jugs halfway and pour them together into a bucket to get 4 liters.', 'reasoning', NULL, NULL, NOW(), 52) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (53, 'Explain the Monty Hall problem: Why is it statistically advantageous to switch doors after the host reveals a goat?', 'When you initially pick a door, you have a 1/3 chance of picking the car and a 2/3 chance of picking a goat. Because the host always reveals a goat behind one of the remaining doors, the 2/3 probability that the car is behind an unchosen door concentrates entirely onto the single remaining closed door. Switching doubles your winning odds from 1/3 to 2/3.', 'It doesn''t matter whether you switch or stay because there are only two doors left, giving you an even 50/50 chance.', 'reasoning', NULL, NULL, NOW(), 53) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (54, 'Three people check into a hotel room costing $30. They each pay $10. Later, the clerk realizes the room was only $25, and gives $5 to the bellboy to return. The bellboy keeps $2 and gives $1 back to each guest. Now each guest paid $9 ($27 total) and the bellboy has $2, totaling $29. Where is the missing dollar?', 'There is no missing dollar; the riddle misdirects by adding when it should subtract. The guests paid $27 total ($30 - $3 refund). Of that $27, $25 went to the hotel register and $2 was pocketed by the bellboy ($25 + $2 = $27). Adding the bellboy''s stolen $2 to the $27 paid is mathematically meaningless.', 'The missing dollar was kept by the front desk clerk as a processing fee.', 'reasoning', NULL, NULL, NOW(), 54) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (55, 'If it takes 8 workers 10 hours to build a brick wall, how many hours would it take 4 workers to build the same wall, assuming identical working speed?', 'It would take 20 hours. Total labor required is 8 workers * 10 hours = 80 worker-hours. With 4 workers, 80 worker-hours / 4 workers = 20 hours.', 'It would take 5 hours because half the workers take half the time.', 'reasoning', NULL, NULL, NOW(), 55) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (56, 'A doctor gives you three pills and tells you to take one every half hour. How many minutes will the pills last?', 'The pills will last 60 minutes. You take pill 1 at minute 0, pill 2 at minute 30, and pill 3 at minute 60.', 'The pills will last 90 minutes because three times thirty minutes is ninety minutes.', 'reasoning', NULL, NULL, NOW(), 56) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (57, 'If Alice is taller than Bob, and Charlie is shorter than Bob, what can we definitively conclude about the height difference between Alice and Charlie?', 'Alice is definitively taller than Charlie. By transitivity: Alice > Bob and Bob > Charlie, therefore Alice > Charlie.', 'We cannot determine who is taller because Charlie''s height is only compared to Bob.', 'reasoning', NULL, NULL, NOW(), 57) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (58, 'You are running in a race and pass the person in second place. What place are you in now?', 'You are in second place. By overtaking the runner who was in second place, you take over their position.', 'You are in first place because you passed the runner ahead of you.', 'reasoning', NULL, NULL, NOW(), 58) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (59, 'A farmer has 17 sheep, and all but 9 die. How many sheep are left alive?', '9 sheep are left alive. The phrase ''all but 9 die'' explicitly states that 9 sheep survived.', '8 sheep are left alive because 17 minus 9 equals 8.', 'reasoning', NULL, NULL, NOW(), 59) ON CONFLICT (id) DO NOTHING;
INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) VALUES (60, 'Is zero an even or odd number, and what is the mathematical proof?', 'Zero is an even number. By definition, an integer n is even if there exists an integer k such that n = 2k. Setting k = 0 yields 2 * 0 = 0. Furthermore, zero is preceded by -1 and succeeded by 1, both of which are odd.', 'Zero is neither even nor odd because it represents nothingness and cannot be divided.', 'reasoning', NULL, NULL, NOW(), 60) ON CONFLICT (id) DO NOTHING;

SELECT setval('labels_id_seq', (SELECT COALESCE(MAX(id), 1) FROM labels));
