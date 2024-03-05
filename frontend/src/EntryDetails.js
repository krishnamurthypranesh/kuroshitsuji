import { React, useEffect, useState } from "react";

import { useNavigate, useParams } from "react-router-dom";

const EntryDetails = (props) => {
    const urlParams = useParams();

    const [entryDetail, setEntryDetail] = useState({ content: {} });

    useEffect(() => { getEntryDetails() }, [])

    const navigate = useNavigate();

    async function getEntryDetails() {
        const userToken = JSON.parse(localStorage.getItem("user")).token;

        const response = await fetch(
            "http://localhost:8000/v1/journal/entries/" + urlParams.entryId,
            {
                method: "GET",
                headers: {
                    Authorization: "Bearer " + userToken,
                    "Content-Type": "application/json",
                },
            }
        )
        if (!response.ok) {
            console.log("error fetching data from server");
            throw new Error("error fetching data from server");
        }

        const data = await response.json();

        console.log(data);

        setEntryDetail(data)
    }

    const renderDetail = () => {
        const data = entryDetail;

        const renderEntryDetail = (data) => {
            return (
                <div>
                <h1>{data.content.title}</h1>
                <p className="lead">{data.content.content}</p>
                </div>
            )
        }

        return (
            <div>{data ? renderEntryDetail(data): <p>Loading...</p>}</div>
        )

    }

    return renderDetail()
}

export default EntryDetails;
