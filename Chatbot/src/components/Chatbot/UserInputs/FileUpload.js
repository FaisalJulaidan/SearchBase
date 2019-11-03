import React, { useEffect, useRef, useState } from 'react';
// Utils
import { validate, genUniqueFileName } from '../../../utils';

// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';

// Components
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTelegramPlane } from '@fortawesome/free-brands-svg-icons';
import { Icon, Progress, Tooltip } from 'antd';

// Styles
import './styles/Inputs.css';
import { getContainerElement } from '../../helpers';

// TO CHANGE
/*
  // USE REF FROM REDUX STATE FOR THE CHATBOTS ID INSTEAD OF DOCUMENT GETELEMENTBYID
*/

const FileUpload = ({ message, submitMessage }) => {
    let [file, setFile] = useState(null);
    let [error, setError] = useState(null);
    let [upload, setUpload] = useState({ progress: 0, uploading: false });
    let [valid, setValid] = useState({ fileExt: true, input: true });
    let fileRef = useRef(null);
    let uploadTimer = useRef(null);

    const fileHandler = (e) => {
        const file = e.target.files[0];
        const fileTypes = message.block[flowAttributes.CONTENT][flowAttributes.FILE_UPLOAD_FILE_TYPES];
        let validator = validate({ input: file, fileTypes }, 'File');

        if (!(validator.valid)) {
            setValid(valid => ({ ...valid, fileExt: false }));
            setError(validator.error);
        } else {
            setFile(file);
            setValid(valid => ({ ...valid, fileExt: true }));
            setError(null);
        }
    };

    const uploadFile = () => {
        if (file && valid.fileExt && !upload.uploading) {
            uploadTimer.current = setInterval(() => {
                setUpload(upload => ({ progress: upload.progress + 5, uploading: true }));
            }, 50);
        }
    };

    useEffect(() => {
        if (upload.progress === 100) {
            clearInterval(uploadTimer.current);
            setUpload(upload => ({ ...upload, progress: 0 }));
            let afterMessage = message.block[flowAttributes.CONTENT][flowAttributes.CONTENT_AFTER_MESSAGE];
            let type = messageTypes.FILE_UPLOAD;
            let text = file.name;
            let block = message.block;
            let newState = {
                curAction: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_ACTION],
                curBlockID: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_BLOCKTOGOID],
                waitingForUser: false
            };
            submitMessage(
                text,
                type,
                newState,
                afterMessage,
                block,
                { skipped: false, file, fileName: genUniqueFileName(file) });
        }
    }, [upload, message, setUpload, file, submitMessage]);

    useEffect(() => {
        if(upload.progress === 0 && upload.uploading === true){
            setUpload(upload => ({...upload, uploading: false}))
            setFile(null)
        }
    }, [upload])

    useEffect(() => {
        return () => clearInterval(uploadTimer.current);
    }, []);

    return (
        <>
            {upload.uploading ?
                <div className={'InputContainer'}>
                    <div className={'Progress'}>
                        <Tooltip placement="top" title={file.name} visible
                                 getPopupContainer={() => getContainerElement()}>
                            <Progress percent={upload.progress} showInfo={false}/>
                        </Tooltip>
                    </div>
                </div>
                :
                <div className={'InputContainer'}>
                    <input
                        className={'Text'} type="text" disabled
                        value={file ? file.name : 'Attach your file...'}
                        placeholder={'Attach your file...'}/>
                </div>
            }
            <>
                <div className={'Actions'}>
                    <Tooltip placement="topRight"
                             getPopupContainer={() => getContainerElement()}
                             title={error}
                             visible={!valid.fileExt}>
                        <i className={!upload.uploading ? 'ClipIconActive' : ''}
                           onClick={() => fileRef.current.click()}>
                            <input ref={fileRef} value="" type="file"
                                   disabled={!valid.input || upload.uploading}
                                   onChange={fileHandler}/>
                            <Icon type="paper-clip" theme="outlined"
                                  style={valid.fileExt ? { fontSize: '22px' } : {
                                      color: 'red',
                                      fontSize: '22px'
                                  }}/>
                        </i>
                    </Tooltip>
                </div>
                <div className={'Submit'}>
                    <i className={file && !upload.uploading ? 'SendIconActive' : ''} onClick={uploadFile}>
                        <FontAwesomeIcon size="2x" icon={faTelegramPlane}/>
                    </i>
                </div>
            </>
        </>
    );
};

export default FileUpload;
