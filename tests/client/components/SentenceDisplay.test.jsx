import React from 'react';
import SentenceDisplay from '../../../client/components/SentenceDisplay.jsx';
import constants from '../../../client/constants.js';
import renderer from 'react-test-renderer';
import {shallow} from 'enzyme';

test("Word selection", () => {
  const onWordChosen = jest.fn();
  const playerSentence = shallow(
    <SentenceDisplay
      words={["One", "two"]} options={["three", "four"]} writing={true}
      guessing={false} isPlayer={true} onWordChosen={onWordChosen} status={constants.GAME_STATUS_WRITING}
    />
  );
  playerSentence.find("button").at(1).simulate("click");
  expect(onWordChosen.mock.calls).toEqual([ [ 1 ] ]);
});

test("No buttons for guessing player", () => {
  const playerSentence = shallow(
    <SentenceDisplay
      words={["One", "two"]} options={["three", "four"]} writing={false}
      guessing={true} isPlayer={true} status={constants.GAME_STATUS_WRITING}
    />
  );
  expect(playerSentence.find("button").exists()).toEqual(false);
})
