const question = document.getElementById('question');
const choices = Array.from(document.getElementsByClassName('choice-text'));
const progressText = document.getElementById('progressText');
const scoreText = document.getElementById('score');
const progressBarFull = document.getElementById('progressBarFull');
const game = document.getElementById('game');
let currentQuestion = {};
let acceptingAnswers = false;
let score = 0;
let questionCounter = 0;
let availableQuesions = [];

const CORRECT_BONUS = 10;
const MAX_QUESTIONS = 10;

// Predefined set of questions
const questions = [
  {
    question: "Do you feel warm, cold, or normal?",
    answer: 1, // 1 for Yes
  },
  {
    question: "Are you experiencing any irregularities or palpitations in your heartbeat?",
    answer: 1, // 1 for Yes
  },
  {
    question: "Have you noticed any changes in your blood pressure recently?",
    answer: 2, // 2 for No
  },
  {
    question: "Are you experiencing any shortness of breath or difficulty breathing?",
    answer: 1, // 1 for Yes
  },
  {
    question: "Are you using any oxygen support, and if so, what is the flow rate?",
    answer: 2, // 2 for No
  },
  {
    question: "Are you experiencing any pain or discomfort?",
    answer: 1, // 1 for Yes
  },
  {
    question: "Have you been in contact with anyone diagnosed with COVID-19 recently?",
    answer: 2, // 2 for No
  },
  {
    question: "Are you currently taking any medications?",
    answer: 1, // 1 for Yes
  },
  {
    question: "Are you experiencing any difficulties falling asleep or staying asleep?",
    answer: 2, // 2 for No
  },
  {
    question: "Are you experiencing any stress, anxiety, or depression symptoms?",
    answer: 1, // 1 for Yes
  },
  // Add more questions as needed
];

startGame = () => {
  questionCounter = 0;
  score = 0;
  availableQuesions = [...questions];
  getNewQuestion();
  game.classList.remove('hidden');
};

getNewQuestion = () => {
  if (availableQuesions.length === 0 || questionCounter >= MAX_QUESTIONS) {
    localStorage.setItem('mostRecentScore', score);
    // Go to the end page
    return window.location.assign('/end.html');
  }
  questionCounter++;
  progressText.innerText = `Question ${questionCounter}/${MAX_QUESTIONS}`;
  progressBarFull.style.width = `${(questionCounter / MAX_QUESTIONS) * 100}%`;

  const questionIndex = Math.floor(Math.random() * availableQuesions.length);
  currentQuestion = availableQuesions[questionIndex];
  question.innerHTML = currentQuestion.question;

  choices.forEach((choice, index) => {
    const choiceText = index === 0 ? 'Yes' : 'No';
    choice.innerHTML = choiceText;
  });

  availableQuesions.splice(questionIndex, 1);
  acceptingAnswers = true;
};

choices.forEach((choice) => {
  choice.addEventListener('click', (e) => {
    if (!acceptingAnswers) return;

    acceptingAnswers = false;
    const selectedChoice = e.target;
    const selectedAnswer = selectedChoice.dataset['number'];

    const classToApply = selectedAnswer == currentQuestion.answer ? 'correct' : 'incorrect';

    if (classToApply === 'correct') {
      incrementScore(CORRECT_BONUS);
    }

    selectedChoice.parentElement.classList.add(classToApply);

    setTimeout(() => {
      selectedChoice.parentElement.classList.remove(classToApply);
      getNewQuestion();
    }, 1000);
  });
});

incrementScore = (num) => {
  score += num;
  scoreText.innerText = score;
};

startGame();
