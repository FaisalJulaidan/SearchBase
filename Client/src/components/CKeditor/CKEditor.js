import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import CKEditor from '@ckeditor/ckeditor5-react';


class CKeditor extends PureComponent {
    constructor(props) {
        super(props)
        this.handleChange = this.handleChange.bind(this)
    }

    handleChange(val) {
        const { onChange } = this.props
        onChange(val)
    }

    render() {
        const { value, disabled, onChange, children, ...others } = this.props
        console.log(disabled)
        return (
            <div>
              <CKEditor
                disabled={disabled}
                data={value}
                config={{toolbar: ['undo', 'redo']}}
                onChange={(event, editor) => this.handleChange(editor?.getData())}
                onInit={editor => this.handleChange(editor?.getData())} {...others } />
            </div>
        )
    }
}

CKeditor.propTypes = {
    onChange: PropTypes.func,
    value: PropTypes.string,
    disabled: PropTypes.oneOfType([
        PropTypes.bool,
        PropTypes.number
    ])
}

export default CKeditor