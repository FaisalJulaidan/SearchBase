import React from 'react';
import PropTypes from 'prop-types';
import PlansTableHead from "./PlansTableHead";
import PlansTableBody from "./PlansTableBody";

const PlansTableSection = props => {
    return (
        <>
            <PlansTableHead index={props.index} sectionKey={props.sectionKey}/>
            <PlansTableBody sectionKey={props.sectionKey}/>
        </>
    );
};

PlansTableSection.propTypes = {
    sectionKey: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired
};

export default PlansTableSection;