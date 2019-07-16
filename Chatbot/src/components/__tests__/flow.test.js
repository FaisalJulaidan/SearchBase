import React from 'react';
import { shallow } from 'enzyme';
import Chatbot from '../Chatbot/Chatbot'
import Button from './Button';

describe('Test Button component', () => {
    it('Test click event', () => {
        const mockCallBack = jest.fn();

        const button = shallow((<Chatbot />));
        console.log(button)
        expect(mockCallBack.mock.calls.length).toEqual(1);
    });
});