import React from 'react';

function FamilyFilter(props) {
    function handleChange(event) {
        props.onChange(event.target.value);

    }
    return(
        <form className="pivot-select-form">
            <div className="pivot-select-container" for="exampleForm.SelectCustom">
                <label>Catégories</label>
                <select value={props.value} onChange={handleChange} as="select" custom>
                <option value={"null"}>Toutes les catégories</option>
            {props.category && props.category.map((option, i) => <option key={i}>{option}</option>)}
                </select>
            </div>
        </form>
    );
}

export default FamilyFilter;