import React from 'react';
import HeadlineInstructions from '../../../client/components/HeadlineInstructions.jsx';
import renderer from 'react-test-renderer';

test("Round 1 writing", () => {
  const component = renderer.create(<HeadlineInstructions round={0} writing={true} guessing={false} />);
  expect(component.toJSON()).toMatchSnapshot();
});

test("Round 2+ writing", () => {
  const component = renderer.create(<HeadlineInstructions round={1} writing={true} guessing={false} />);
  expect(component.toJSON()).toMatchSnapshot();
});

test("Round 1 guessing", () => {
  const component = renderer.create(<HeadlineInstructions round={0} writing={false} guessing={true} />);
  expect(component.toJSON()).toMatchSnapshot();
});

test("Round 2+ guessing", () => {
  const component = renderer.create(<HeadlineInstructions round={1} writing={false} guessing={true} />);
  expect(component.toJSON()).toMatchSnapshot();
});
