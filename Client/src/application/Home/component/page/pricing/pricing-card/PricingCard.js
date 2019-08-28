import React from 'react';
import styles from './pricing-card.module.css';
import {Card} from "react-bootstrap";
import Button from "react-bootstrap/Button";

const PricingCard = () => {
    return (
        <div>
            <Card className={styles.card}>
                <Card.Header className={styles.header}>
                    <h1>Basic Plan</h1>
                </Card.Header>
                <Card.Body>
                    <ul style={{
                        listStyleType: 'disc',
                        listStylePosition: 'inside'
                    }}>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                        <li>Unlimited Chatbot agents</li>
                    </ul>
                    <Button style={{margin:'2em'}}>Buy Now!</Button>
                </Card.Body>
            </Card>
        </div>
    );
};

export default PricingCard;
