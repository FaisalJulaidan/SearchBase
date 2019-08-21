import {Component} from 'react'
import {withRouter} from "react-router-dom";
import {animateScroll, scroller} from "react-scroll";

class ScrollTo extends Component {


    componentDidUpdate(prevProps) {
        if (this.props.location.hash === "")
            if (this.props.location.pathname !== prevProps.location.pathname) {
                window.scrollTo(0, 0);
            } else {
                animateScroll.scrollToTop();
            }
        else {
            if (this.props.location.pathname !== prevProps.location.pathname) {
                scroller.scrollTo(this.props.location.hash.replace("#", ""))
            } else {
                scroller.scrollTo(this.props.location.hash.replace("#", ""), {
                    duration: 1000,
                    delay: 100,
                    smooth: true,
                })
            }

        }
    }


    render() {
        return this.props.children;
    }
}

export default withRouter(ScrollTo);