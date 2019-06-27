import React from 'react';
import {Button, Popconfirm} from "antd";

export const DefaultButton = ({
                                  disconnectMarketplace,
                                  isDisconnecting,
                                  showModal,
                                  status,
                              }) =>
    <>
        {
            (status === "CONNECTED" || status === "FAILED")
            &&
            <Popconfirm placement={'bottomRight'}
                        title="Chatbot conversations will no longer be synced with Adapt account"
                        onConfirm={disconnectMarketplace}
                        okType={'danger'}
                        okText="Disconnect"
                        cancelText="No">
                <Button type="danger"
                        style={{width: 'auto'}}
                        size={'large'}
                        disabled={isDisconnecting}>
                    {
                        status === "FAILED" ? '(Failed) click to disconnect' : 'Disconnect'
                    }
                </Button>
            </Popconfirm>
        }

        {
            status === "NOT_CONNECTED" &&
            <Button type="primary"
                    icon={'login'}
                    onClick={showModal}
                    size={'large'}>Connect</Button>
        }
    </>;
