import React from 'react';
import terms from './terms.json';
import {WEBSITE_TITLE} from '../../../../../constants/config';
import DescriptiveLayout from "../../../hoc/descriptive-layout/DescriptiveLayout";

const Terms = () => {

    document.title = "Terms & Conditions | " + WEBSITE_TITLE;

    return (
        <DescriptiveLayout title="Terms & Conditions" items={terms}/>
    );
};

export default Terms;
