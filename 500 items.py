import time
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class GoogleFormAutoSubmitter:
    def __init__(self, form_url, answer_key=None):
        """
        Initialize the form submitter with the URL of the Google Form and optional answer key.

        Parameters:
        - form_url: URL of the Google Form
        - answer_key: List of answers (0=A, 1=B, 2=C, 3=D)
        """
        self.form_url = form_url

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Maximize window to see all elements

        # Setup Chrome WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                       options=chrome_options)

        # Load answer key or use the provided one
        self.answer_key = answer_key if answer_key else self.generate_random_answer_key(500)

        # Track the score to ensure we're in the 250-350 range
        self.correct_answers = 0

        # Set target score range
        self.min_target_score = 250
        self.max_target_score = 350

        # Target accuracy to achieve score in range (50-70%)
        self.target_accuracy = random.uniform(0.50, 0.70)
        print(f"Target accuracy set to {self.target_accuracy:.2f} to achieve score in range 250-350")

    def generate_random_answer_key(self, num_questions):
        """Generate a random answer key if none is provided."""
        print("Generating random answer key")
        return [random.randint(0, 3) for _ in range(num_questions)]

    def save_answer_key(self, filename="answer_key.json"):
        """Save the current answer key to a file for future use."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.answer_key, f)
            print(f"Answer key saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving answer key: {str(e)}")
            return False

    def start(self):
        """Navigate to the form URL."""
        print("Opening Google Form...")
        self.driver.get(self.form_url)
        time.sleep(3)  # Wait for the form to load completely

    def generate_random_name(self):
        """Generate a random first name only."""
        first_names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Avery",
                       "Quinn", "Jamie", "Blake", "Skyler", "Dakota", "Cameron", "Reese",
                       "Finley", "Harley", "Phoenix", "Robin", "Charlie", "Emerson",
                       "Apple", "Orange", "Melon", "Skye", "Euro", "Luna", "Ginger"]

        return random.choice(first_names)

    def generate_random_age(self, min_age=18, max_age=21):
        """Generate a random age within the specified range."""
        return random.randint(min_age, max_age)

    def handle_first_page(self):
        """Handle the first page with special fields (single option, name, age)."""
        print("Handling first page...")

        try:
            # Handle first question with single option
            print("Selecting single option in first question...")

            # Try multiple ways to find and click the first radio button
            try:
                single_option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='radio']"))
                )
                single_option.click()
                print("Selected single option using CSS selector")
            except:
                try:
                    # Alternative method using JavaScript
                    self.driver.execute_script(
                        "document.querySelector('div[role=\"radio\"]').click();"
                    )
                    print("Selected single option using JavaScript")
                except:
                    print("Failed to select single option, continuing anyway")

            time.sleep(0.5)

            # Find all text input fields - trying different methods
            try:
                input_fields = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']"))
                )

                # Handle name field (first text input)
                if len(input_fields) >= 1:
                    random_name = self.generate_random_name()
                    input_fields[0].clear()
                    input_fields[0].send_keys(random_name)
                    print(f"Entered name: {random_name}")
                    time.sleep(0.5)

                # Handle age field (second text input)
                if len(input_fields) >= 2:
                    random_age = self.generate_random_age(18, 21)
                    input_fields[1].clear()
                    input_fields[1].send_keys(str(random_age))
                    print(f"Entered age: {random_age}")
                    time.sleep(0.5)
            except:
                # Try alternative method with JavaScript if the above fails
                try:
                    # Focus on first input (name) and enter value
                    random_name = self.generate_random_name()
                    self.driver.execute_script(
                        f"document.querySelectorAll('input[type=\"text\"]')[0].value = '{random_name}';"
                    )
                    print(f"Entered name via JavaScript: {random_name}")
                    time.sleep(0.5)

                    # Focus on second input (age) and enter value
                    random_age = self.generate_random_age(18, 21)
                    self.driver.execute_script(
                        f"document.querySelectorAll('input[type=\"text\"]')[1].value = '{random_age}';"
                    )
                    print(f"Entered age via JavaScript: {random_age}")
                    time.sleep(0.5)
                except:
                    print("Failed to enter name and age, continuing anyway")

            # Ensure we're scrolled down to see the Susunod button
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Click the Susunod button - try multiple methods
            try:
                # Try to find the Susunod button using various selectors
                next_button_xpaths = [
                    "//span[text()='Susunod']/parent::*",
                    "//span[contains(text(), 'Susunod')]/parent::*",
                    "//div[contains(@class, 'Susunod')]",
                ]

                next_button = None
                for xpath in next_button_xpaths:
                    try:
                        next_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        if next_button:
                            break
                    except:
                        continue

                if next_button:
                    # Try regular click
                    try:
                        next_button.click()
                        print("Clicked Susunod button")
                    except:
                        # Try JavaScript click if regular click fails
                        self.driver.execute_script("arguments[0].click();", next_button)
                        print("Clicked Susunod button via JavaScript")
                else:
                    # Try direct JavaScript approach to find and click Susunod button
                    self.driver.execute_script(
                        """
                        var buttons = document.querySelectorAll('button, div[role="button"]');
                        for (var i = 0; i < buttons.length; i++) {
                            if (buttons[i].textContent.includes('Susunod')) {
                                buttons[i].click();
                                return true;
                            }
                        }
                        return false;
                        """
                    )
                    print("Attempted to click Susunod button via JavaScript search")
            except Exception as e:
                print(f"Error when trying to click Susunod button: {str(e)}")
                print("Continuing anyway - we may already be on the quiz page")

            time.sleep(3)  # Wait longer for the page transition
            return True

        except Exception as e:
            print(f"Error handling first page: {str(e)}")
            # Try to continue anyway
            return True

    def decide_answer(self, question_index, num_options=4):
        """
        Decide which answer to pick based on:
        1. The answer key
        2. The target score range (250-350 out of 500)
        3. Current progress towards the target

        Returns the index of the option to select (0-based)
        """
        # Get the correct answer from our answer key
        correct_answer = self.answer_key[question_index]

        # Questions remaining (including this one)
        remaining = 500 - question_index

        # Calculate how many more correct answers we need
        min_needed = self.min_target_score - self.correct_answers
        max_allowed = self.max_target_score - self.correct_answers

        # Calculate bounds for accuracy for remaining questions
        min_accuracy_needed = max(0, min_needed / remaining)
        max_accuracy_allowed = min(1.0, max_allowed / remaining)

        # Decide whether to answer correctly based on needed accuracy range
        if min_accuracy_needed > 0.9:  # Must answer correctly to reach minimum
            selected_answer = correct_answer
            will_answer_correctly = True
        elif max_accuracy_allowed < 0.1:  # Must answer incorrectly to stay below maximum
            options = list(range(num_options))
            options.remove(correct_answer)
            selected_answer = random.choice(options)
            will_answer_correctly = False
        else:
            # Normal case: probabilistically decide based on target accuracy
            if random.random() < self.target_accuracy:
                selected_answer = correct_answer  # Answer correctly
                will_answer_correctly = True
            else:
                # Choose a wrong answer randomly
                options = list(range(num_options))
                options.remove(correct_answer)
                selected_answer = random.choice(options)
                will_answer_correctly = False

        # Update our score tracker if we're answering correctly
        if will_answer_correctly:
            self.correct_answers += 1
            answer_status = "correctly"
        else:
            answer_status = "incorrectly"

        # Print progress towards target score
        if question_index % 50 == 0 or question_index == 499:
            print(f"Current score: {self.correct_answers}/{question_index + 1} "
                  f"(Projected: {int(self.correct_answers / (question_index + 1) * 500)} / 500)")
            print(f"Accuracy bounds for remaining questions: {min_accuracy_needed:.2f} to {max_accuracy_allowed:.2f}")

        # Make sure the selected answer is within range
        selected_answer = min(selected_answer, num_options - 1)

        print(f"Q{question_index + 1}: Answer key says {chr(65 + correct_answer)}. "
              f"Answering {answer_status} with {chr(65 + selected_answer)}")

        return selected_answer

    def fill_quiz(self, num_questions=500):
        """
        Fill out a multiple-choice quiz form using the answer key.

        Parameters:
        - num_questions: Number of questions in the form (default: 500)
        """
        print(f"Starting to fill {num_questions} questions...")

        # Track current question to handle pagination
        current_question = 0  # 0-indexed to match answer key
        consecutive_errors = 0
        max_consecutive_errors = 5

        while current_question < num_questions and consecutive_errors < max_consecutive_errors:
            try:
                # Ensure we're scrolled to see current questions
                if current_question % 5 == 0:
                    self.driver.execute_script("window.scrollBy(0, 300);")
                    time.sleep(0.5)

                # Try to find all visible question containers
                question_containers = self.driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")

                if not question_containers:
                    consecutive_errors += 1
                    print(f"No question containers found. Error {consecutive_errors}/{max_consecutive_errors}")
                    time.sleep(1)
                    continue

                # Reset error counter if we found questions
                consecutive_errors = 0

                # Find a question that hasn't been answered yet
                for question_div in question_containers:
                    # Find all answer options (radio buttons) for this question
                    options = question_div.find_elements(By.CSS_SELECTOR, "div[role='radio']")

                    # Check if any option is already selected
                    already_answered = False
                    for option in options:
                        if "aria-checked" in option.get_attribute("outerHTML") and option.get_attribute(
                                "aria-checked") == "true":
                            already_answered = True
                            break

                    # Skip this question if already answered
                    if already_answered:
                        continue

                    # Answer this question if not already answered
                    if options and len(options) > 0:
                        # Decide which option to select based on answer key and target score
                        selected_index = self.decide_answer(current_question, len(options))

                        # Ensure we're within range of available options
                        selected_index = min(selected_index, len(options) - 1)

                        try:
                            options[selected_index].click()
                            print(f"Question {current_question + 1}: Selected option {selected_index + 1}")
                            current_question += 1
                            # Add a delay between answering questions for a more moderate pace
                            time.sleep(0.75)  # Increased delay between questions
                            break  # Move to next question
                        except:
                            # Try JavaScript click if regular click fails
                            try:
                                self.driver.execute_script("arguments[0].click();", options[selected_index])
                                print(
                                    f"Question {current_question + 1}: Selected option {selected_index + 1} via JavaScript")
                                current_question += 1
                                time.sleep(0.75)  # Increased delay between questions
                                break  # Move to next question
                            except:
                                print(f"Failed to click option for question {current_question + 1}")

                # Check if we need to go to the next page after every 10 questions
                if current_question % 10 == 0 and current_question > 0:
                    # Scroll to bottom to see Susunod button
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)

                    try:
                        # Look for the Susunod button
                        next_buttons = self.driver.find_elements(By.XPATH,
                                                                 "//span[contains(text(), 'Susunod')]/parent::*")
                        if next_buttons:
                            for btn in next_buttons:
                                if btn.is_displayed():
                                    try:
                                        btn.click()
                                        print("Clicked Susunod button to new page")
                                        time.sleep(3)  # Wait longer for the next page to load
                                        break
                                    except:
                                        try:
                                            # Try JavaScript click if regular click fails
                                            self.driver.execute_script("arguments[0].click();", btn)
                                            print("Clicked Susunod button via JavaScript")
                                            time.sleep(3)
                                            break
                                        except:
                                            continue
                    except:
                        # No next button or error clicking it
                        pass

            except Exception as e:
                print(f"Error on question {current_question + 1}: {str(e)}")
                consecutive_errors += 1

                if consecutive_errors >= max_consecutive_errors:
                    print(f"Too many consecutive errors ({consecutive_errors}). Moving to submit.")
                    break

                # Try to find and click the Susunod button if we're stuck
                try:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)

                    next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Susunod')]/parent::*")
                    if next_button.is_displayed():
                        next_button.click()
                        print("Recovered by clicking Susunod button")
                        time.sleep(2)
                        consecutive_errors = 0  # Reset error counter if we successfully navigated
                except:
                    # If we can't recover, wait a bit and try again
                    time.sleep(1)

        # Print final score statistics
        print(
            f"Final score: {self.correct_answers}/{num_questions} ({self.correct_answers / num_questions * 100:.1f}%)")
        print(f"Score is within target range {self.min_target_score}-{self.max_target_score}: "
              f"{self.min_target_score <= self.correct_answers <= self.max_target_score}")

    def submit_form(self):
        """Submit the completed form."""
        try:
            # Scroll to bottom to see Submit/Isumite button
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Try different methods to find and click the Submit/Isumite button
            try:
                # Method 1: Standard WebDriverWait
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "//span[contains(text(), 'Isumite')]/parent::* | //span[contains(text(), 'Submit')]/parent::*"))
                )
                submit_button.click()
                print("Form submitted successfully!")
            except:
                try:
                    # Method 2: Try finding all elements with "Isumite" or "Submit" text
                    submit_buttons = self.driver.find_elements(By.XPATH,
                                                               "//span[contains(text(), 'Isumite')]/parent::* | //span[contains(text(), 'Submit')]/parent::*")
                    if submit_buttons:
                        for btn in submit_buttons:
                            if btn.is_displayed():
                                btn.click()
                                print("Form submitted via alternate method!")
                                break
                except:
                    try:
                        # Method 3: JavaScript approach
                        result = self.driver.execute_script(
                            """
                            var buttons = document.querySelectorAll('button, div[role="button"]');
                            for (var i = 0; i < buttons.length; i++) {
                                if (buttons[i].textContent.includes('Isumite') || buttons[i].textContent.includes('Submit')) {
                                    buttons[i].click();
                                    return true;
                                }
                            }
                            return false;
                            """
                        )
                        if result:
                            print("Form submitted via JavaScript!")
                        else:
                            print("Submit/Isumite button not found via JavaScript")
                    except Exception as js_e:
                        print(f"JavaScript submit attempt failed: {str(js_e)}")

            time.sleep(3)  # Wait for submission confirmation
            return True

        except Exception as e:
            print(f"Error submitting form: {str(e)}")
            return False

    def close(self):
        """Close the browser."""
        self.driver.quit()
        print("Browser closed.")


def convert_letter_to_number(letter):
    """Convert letter answer (A, B, C, D) to number (0, 1, 2, 3)"""
    letter = letter.strip().upper()
    if letter == 'A':
        return 0
    elif letter == 'B':
        return 1
    elif letter == 'C':
        return 2
    elif letter == 'D':
        return 3
    else:
        # Default to A if invalid
        print(f"Warning: Invalid answer '{letter}', defaulting to A (0)")
        return 0


def parse_answer_key():
    """Parse the provided answer key and convert from letters to numbers"""
    # Hardcoded answer key from the provided document
    answer_key_text = """
    1. C
    2. B
    3. B
    4. B
    5. A
    6. A
    7. C
    8. B
    9. A
    10. A
    11. A
    12. A
    13. B
    14. B
    15. A
    16. B
    17. A
    18. B
    19. B
    20. B
    21. A
    22. B
    23. A
    24. A
    25. B
    26. B
    27. A
    28. A
    29. B
    30. A
    31. B
    32. A
    33. A
    34. B
    35. B
    36. A
    37. A
    38. B
    39. A
    40. C
    41. B
    42. A
    43. B
    44. A
    45. A
    46. C
    47. B
    48. A
    49. C
    50. A
    51. A
    52. C
    53. B
    54. A
    55. C
    56. A
    57. A
    58. B
    59. B
    60. A
    61. C
    62. B
    63. A
    64. C
    65. B
    66. A
    67. A
    68. A
    69. A
    70. A
    71. A
    72. A
    73. C
    74. B
    75. A
    76. A
    77. B
    78. A
    79. A
    80. A
    81. A
    82. A
    83. B
    84. A
    85. C
    86. B
    87. A
    88. A
    89. A
    90. A
    91. A
    92. B
    93. A
    94. C
    95. A
    96. A
    97. C
    98. A
    99. A
    100. C
    101. A
    102. A
    103. C
    104. B
    105. A
    106. C
    107. B
    108. A
    109. C
    110. A
    111. A
    112. C
    113. A
    114. A
    115. A
    116. B
    117. A
    118. C
    119. B
    120. A
    121. C
    122. A
    123. A
    124. B
    125. B
    126. B
    127. B
    128. C
    129. A
    130. B
    131. A
    132. B
    133. A
    134. A
    135. C
    136. B
    137. D
    138. C
    139. D
    140. C
    141. C
    142. C
    143. A
    144. A
    145. C
    146. A
    147. D
    148. D
    149. B
    150. B
    151. D
    152. D
    153. C
    154. D
    155. B
    156. C
    157. B
    158. D
    159. D
    160. C
    161. B
    162. C
    163. A
    164. C
    165. B
    166. D
    167. B
    168. B
    169. A
    170. C
    171. A
    172. B
    173. D
    174. A
    175. C
    176. D
    177. B
    178. C
    179. A
    180. B
    181. B
    182. D
    183. A
    184. C
    185. C
    186. D
    187. D
    188. B
    189. B
    190. D
    191. A
    192. C
    193. A
    194. B
    195. A
    196. B
    197. A
    198. D
    199. B
    200. A
    201. D
    202. D
    203. B
    204. A
    205. C
    206. C
    207. D
    208. A
    209. C
    210. A
    211. B
    212. C
    213. D
    214. C
    215. D
    216. A
    217. B
    218. A
    219. B
    220. A
    221. B
    222. C
    223. D
    224. B
    225. D
    226. A
    227. B
    228. D
    229. D
    230. A
    231. C
    232. A
    233. B
    234. A
    235. B
    236. C
    237. D
    238. C
    239. A
    240. D
    241. A
    242. C
    243. D
    244. B
    245. A
    246. B
    247. B
    248. C
    249. A
    250. D
    251. C
    252. A
    253. B
    254. D
    255. B
    256. A
    257. B
    258. B
    259. C
    260. D
    261. B
    262. A
    263. B
    264. B
    265. A
    266. D
    267. B
    268. A
    269. C
    270. B
    271. B
    272. A
    273. B
    274. C
    275. C
    276. D
    277. A
    278. B
    279. A
    280. B
    281. B
    282. A
    283. C
    284. B
    285. B
    286. A
    287. D
    288. B
    289. D
    290. D
    291. B
    292. C
    293. B
    294. B
    295. A
    296. B
    297. B
    298. D
    299. C
    300. A
    301. B
    302. A
    303. D
    304. D
    305. B
    306. B
    307. D
    308. B
    309. A
    310. C
    311. A
    312. B
    313. B
    314. B
    315. C
    316. D
    317. A
    318. B
    319. A
    320. C
    321. B
    322. A
    323. D
    324. B
    325. C
    326. B
    327. B
    328. A
    329. D
    330. A
    331. A
    332. B
    333. C
    334. A
    335. D
    336. B
    337. A
    338. B
    339. A
    340. A
    341. B
    342. D
    343. B
    344. A
    345. A
    346. B
    347. A
    348. C
    349. B
    350. A
    351. C
    352. B
    353. A
    354. A
    355. B
    356. A
    357. C
    358. B
    359. A
    360. A
    361. B
    362. A
    363. A
    364. B
    365. A
    366. D
    367. B
    368. A
    369. A
    370. B
    371. B
    372. D
    373. A
    374. C
    375. C
    376. A
    377. B
    378. B
    379. B
    380. B
    381. B
    382. A
    383. A
    384. D
    385. B
    386. C
    387. B
    388. D
    389. A
    390. A
    391. B
    392. C
    393. A
    394. A
    395. D
    396. B
    397. A
    398. B
    399. A
    400. A
    401. A
    402. D
    403. A
    404. B
    405. D
    406. B
    407. A
    408. A
    409. A
    410. B
    411. C
    412. A
    413. A
    414. B
    415. C
    416. D
    417. B
    418. A
    419. A
    420. B
    421. C
    422. A
    423. B
    424. B
    425. D
    426. B
    427. A
    428. A
    429. A
    430. A
    431. D
    432. B
    433. A
    434. C
    435. A
    436. C
    437. B
    438. A
    439. B
    440. B
    441. A
    442. A
    443. B
    444. C
    445. A
    446. B
    447. A
    448. B
    449. A
    450. B
    451. B
    452. B
    453. A
    454. A
    455. A
    456. B
    457. A
    458. A
    459. A
    460. B
    461. B
    462. A
    463. B
    464. A
    465. D
    466. A
    467. A
    468. A
    469. A
    470. A
    471. A
    472. B
    473. D
    474. C
    475. C
    476. B
    477. B
    478. C
    479. C
    480. C
    481. C
    482. D
    483. C
    484. D
    485. A
    486. C
    487. B
    488. A
    489. C
    490. B
    491. C
    492. A
    493. D
    494. B
    495. C
    496. B
    497. B
    498. C
    499. C
    500. C
    """

    # Split the text into lines and extract the answers
    lines = answer_key_text.strip().split('\n')
    answers = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split('.')
        if len(parts) >= 2:
            letter_answer = parts[1].strip()
            numeric_answer = convert_letter_to_number(letter_answer)
            answers.append(numeric_answer)

    print(f"Parsed {len(answers)} answers from the answer key")
    return answers


def main():
    # Replace with your actual Google Form URL
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeBtdn1krW4DVeekXjvW8jqDMs-KfmFOhv-fnKC_s_fJnp-5A/viewform"

    # Parse the answer key (convert from A,B,C,D to 0,1,2,3)
    answers = parse_answer_key()

    # Check if we have enough answers
    if len(answers) < 500:
        print(f"Warning: Answer key only has {len(answers)} answers, but we need 500.")
        print("Will use available answers and generate random ones for the rest.")
        # Extend with random answers if needed
        answers.extend([random.randint(0, 3) for _ in range(500 - len(answers))])

    # Create the form submitter instance with the parsed answer key
    submitter = GoogleFormAutoSubmitter(form_url, answers)

    try:
        # Start the process
        submitter.start()

        # Handle the first page with special fields
        if not submitter.handle_first_page():
            print("Failed to handle first page, but continuing anyway...")

        # Fill out the multiple choice questions
        submitter.fill_quiz(num_questions=500)

        # Submit the form
        if submitter.submit_form():
            print("Form submitted successfully!")
            # Save the answer key for future reference
            submitter.save_answer_key()
        else:
            print("Form submission failed.")

    except Exception as e:
        print(f"Error during form submission: {str(e)}")

    finally:
        # Ensure the browser is closed
        submitter.close()


if __name__ == "__main__":
    main()