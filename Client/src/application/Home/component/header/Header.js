import React from 'react';
import styles from './header.module.css';
import {Container, Navbar, Nav, NavDropdown, Button} from "react-bootstrap";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCloud} from "@fortawesome/free-solid-svg-icons";

const Header = (props) => {
    return (
        <header id={props.id} className={styles.header}>
            <Navbar collapseOnSelect expand="md" sticky="top">
                <Container>
                    <Link style={{textDecoration: 'none'}} to="/">
                        <div className={styles.logo}>
                            <FontAwesomeIcon size="2x" icon={faCloud}/>
                            <h1>SearchBase</h1>
                        </div>
                    </Link>
                    <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                    <Navbar.Collapse>
                        <Nav className={styles.nav_buttons}>
                            <NavDropdown id="products" className={styles.link_dropdown} title="Products">
                                <NavDropdown.Item className={styles.link} as={Link}
                                                  to={{pathname: "/how-it-works", hash: "#chatbot",}}>Chatbot
                                </NavDropdown.Item>
                                <NavDropdown.Item className={styles.link} as={Link}
                                                  to={{pathname: "/how-it-works", hash: "#candidate",}}>Candidate
                                    Activation
                                </NavDropdown.Item>
                                <NavDropdown.Item className={styles.link} as={Link}
                                                  to={{pathname: "/how-it-works", hash: "#sms",}}>SMS Outreach
                                </NavDropdown.Item>
                                <NavDropdown.Item className={styles.link} as={Link}
                                                  to={{pathname: "/how-it-works", hash: "#engagement",}}>Engagement
                                </NavDropdown.Item>
                            </NavDropdown>
                            <Nav.Link className={styles.link} as={Link} to="/how-it-works">How it works?</Nav.Link>
                            <Nav.Link className={styles.link} as={Link} to="/pricing">Pricing</Nav.Link>
                            <Nav.Link className={styles.link} as={Link} to="/login">Log in</Nav.Link>
                        </Nav>
                        <div className={styles.button_wrapper}>
                            <Link to="/get-started">
                                <Button className={styles.button} variant="light">
                                    Book a demo
                                </Button>
                            </Link>
                        </div>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </header>);
};

export default Header;
