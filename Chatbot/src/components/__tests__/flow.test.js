import React from 'react';
import { shallow } from 'enzyme';
import { cleanup, render } from '@testing-library/react'
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'

import mockData from './mockFlow.json'

import {getServerDomain} from "../../utils";
import { Chatbot }   from '../Chatbot/Chatbot'
import {initialState as state} from '../../store/reducers/chatbot'


describe('Chatbot', () => {
    it('Renders the chatbot', () => {
        const component = shallow (<Chatbot/>);
        expect(component).toHaveLength(1)
    });

    it('Fetches and initiates chatbot', () => {
        const mockInitiateChatbot = jest.fn();
        const mockSetChatbotStatus = jest.fn();
        const mock = new MockAdapter(axios)

        mock.onGet(`${getServerDomain()}/api/assistant/1235/chatbot`).reply(200, mockData)


        const { rerender } = shallow(<Chatbot assistantID={1235} chatbot={{...state}}  initChatbot={mockInitiateChatbot} setChatbotStatus={mockSetChatbotStatus}/>);
        // rerender
        const { assistant } = mockData.data;

        expect(mockInitiateChatbot.mock.calls[0][0]).toBe(assistant);
        expect(mockInitiateChatbot.mock.calls[0][1]).toBe([].concat(assistant.Flow.groups.map(group => group.blocks)).flat(1))
        expect(mockInitiateChatbot.mock.calls[0][2]).toBe({ disabled: isBlocked, active: assistant.Active })
    });
});


describe('Chatbot animation', () => {
    it('Chatbot animation opens on init', () => {
        const mockCallBack = jest.fn();

        const button = shallow((<Chatbot />));
        console.log(button)
        expect(mockCallBack.mock.calls.length).toEqual(1);
    });
});

// TESTS TO WRITE
/*
    - CHECK CHATBOT IS DISABLED
    - CHECK CHATBOT

 */