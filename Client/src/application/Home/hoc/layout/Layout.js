import React, {Component} from 'react'
import '../../bootstrap.css'
import './layout.css'
import Header from "../../component/header/Header";
import Footer from '../../component/footer/Footer'
import {StickyContainer} from "react-sticky";
import PropTypes from "prop-types";

class Layout extends Component {

    render() {
        return (
            <StickyContainer id="content-wrap" style={{background: this.props.background}}>
                <Header id="header"/>
                {this.props.children}
                <Footer background={this.props.background} id="footer"/>
            </StickyContainer>
        )
    }
}

Layout.propTypes = {
    background: PropTypes.string
};

export default Layout