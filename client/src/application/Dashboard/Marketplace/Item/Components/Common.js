import React from 'react';
import {Button, Popconfirm} from "antd";

export const DefaultButton = ({
                                  buttonText,
                                  icon,
                                  windowObject = {},
                                  disconnectMarketplace,
                                  isDisconnecting,
                                  showModal,
                                  status,
                                  isConnecting
                              }) =>
    <>
        {
            (status === "CONNECTED" || status === "FAILED")
            &&
            <Popconfirm placement={'bottomRight'}
                        title="Chatbot conversations will no longer be synced with your account"
                        onConfirm={disconnectMarketplace}
                        okType={'danger'}
                        okText="Disconnect"
                        cancelText="No">
                <Button type="danger"
                        style={{width: 'auto'}}
                        size={'large'}
                        loading={isDisconnecting}>
                    {
                        status === "FAILED" ? '(Failed) click to disconnect' : 'Disconnect'
                    }
                </Button>
            </Popconfirm>
        }

        {
            status === "NOT_CONNECTED" &&
            <Button type="primary"
                    icon={icon ? icon : 'login'}
                    style={{width: 'auto'}}
                    loading={isConnecting}
                    onClick={() => {
                        if (windowObject.url)
                            return window.open(windowObject.url, windowObject.target, windowObject.features);
                        else
                            return showModal()
                    }}
                    size={'large'}>
                {
                    isConnecting ? 'Pinging...' : buttonText
                }

            </Button>
        }
    </>;

