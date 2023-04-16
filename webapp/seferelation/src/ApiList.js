import React, { useState, useEffect } from 'react';


function ApiList() {
    const [data, setData] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetch(`http://localhost:8000/relations?sefaria_link=${searchTerm}`)
            .then(response => response.json())
            .then(data => setData(data));
    }, [searchTerm]);

    function handleSearchChange(event) {
        setSearchTerm(event.target.value);
    }

    return (
        <div>
        <h1>API List</h1>
        <label>
        Search relations with seferelation api (by @ykaner):
        <input type="text" value={searchTerm} onChange={handleSearchChange} />
        </label>
        <ul>
        {data.map(item => (
            <li key={item.id}>{item.name}</li>
        ))}
        </ul>
        </div>
    );
}

export default ApiList;

