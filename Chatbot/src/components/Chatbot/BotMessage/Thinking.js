import React from 'react';
import './styles/Thinking.css';
import '../styles/Animations.css';

const Thinking = () => {
    return (
        <div className={`${'Thinking'} ${'BounceIn'}`}>
            <div className={'ParentDots'}>
                <div className={'Dots'}/>
                <div className={'Dots'}/>
                <div className={'Dots'}/>
            </div>
        </div>
    );
};

export default Thinking;
