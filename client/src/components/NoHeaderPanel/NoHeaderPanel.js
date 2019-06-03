import React, {Component} from 'react';
import styles from "./NoHeaderPanel.module.less";


class NoHeaderPanel extends Component {

    constructor(props) {
        super(props);
        this.updateElementsDimensions = this.updateElementsDimensions.bind(this)
    }

    TitleElementRef = {};
    BodyElementRef = {};

    componentDidMount() {
        // window.addEventListener('resize', this.updateElementsDimensions);
        // setTimeout(
        //     () => this.BodyElementRef.style.height = `calc(100% - ${this.TitleElementRef.clientHeight}px)`,
        //     1
        // );
    }

    componentWillUnmount() {
        // window.removeEventListener('resize', this.updateElementsDimensions)
    }

    updateElementsDimensions() {
        // this.BodyElementRef.style.height = `calc(100% - ${this.TitleElementRef.clientHeight}px)`
    }

    render() {
        console.log(this.props);
        const TitleElement = React.Children.only(this.props.children[0]);
        const BodyElement = React.Children.only(this.props.children[1]);

        return (
            this.props.loading ?
                null
                :
                <div style={{height: '100%'}}>
                    <div className={styles.Panel}>
                        <div className={styles.Panel_Body}>
                            {React.cloneElement(TitleElement, {ref: el => this.TitleElementRef = el})}
                            {React.cloneElement(BodyElement, {ref: el => this.BodyElementRef = el})}
                        </div>
                    </div>
                </div>
        );
    }
}

export default NoHeaderPanel;
