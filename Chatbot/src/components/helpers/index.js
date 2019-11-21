export const getContainerElement = () => {
    if (document.getElementById('TheSearchBase_Chatbot_Input'))
        return document.getElementById('TheSearchBase_Chatbot_Input');
    else
        return document.getElementById('TheSearchBase_Chatbot');
};
