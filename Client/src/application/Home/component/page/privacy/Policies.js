import React from 'react';
import policies from './policies.json';
import {WEBSITE_TITLE} from '../../../../../constants/config';
import DescriptiveLayout from "../../../hoc/descriptive-layout/DescriptiveLayout";

const Policies = () => {

    document.title = "Privacy Policy | " + WEBSITE_TITLE;

    return (
        <DescriptiveLayout title="Privacy Policy" items={policies}/>
    );
};

export default Policies;
