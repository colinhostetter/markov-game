const constants = {
  COOKIE_NAME: "markov",
  
  ROUNDS_PER_GAME: 10,
  WORDS_PER_SENTENCE: 10,

  WORD_CHOICE_TIME_SECONDS: 3,
  FIRST_WORD_CHOICE_TIME_SECONDS: 5,
  GUESS_TIME_SECONDS: 10,

  GAME_STATUS_PREGAME: "pregame",
  GAME_STATUS_WRITING: "writing",
  GAME_STATUS_GUESS_TIME: "guess_time",
  GAME_STATUS_REVEAL: "reveal",
  GAME_STATUS_POSTGAME: "postgame",
};

export default constants;
