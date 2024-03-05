import { React, useEffect, useState } from "react";

import { useNavigate, useParams } from "react-router-dom";

const CollectionDetails = (props) => {
    const urlParams = useParams();

    const [entriesList, setEntriesList] = useState({ records: [] });

    useEffect(() => { listEntriesForCollection() }, [])

    const navigate = useNavigate();

    const onAddEntryButtonClick = () => {
        // navigate to the concerned url
        navigate("/collections/" + urlParams.collectionId + "/new-entry/")
    }

    async function listEntriesForCollection() {
        const userToken = JSON.parse(localStorage.getItem("user")).token;

        const response = await fetch(
            "http://localhost:8000/v1/journal/entries/?collection_id=" + urlParams.collectionId,
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

        setEntriesList(data)
    }

    const renderTable = () => {
        const data = entriesList;

        const generateRow = (record, index) => {
            return (
                <tr>
                        <td>{index + 1}</td>
                        <td><a href={"/entries/" + record.entry_id}>{record.entry_id}</a></td>
                        <td>{record.title}</td>
                        <td>{record.created_at}</td>
                        <td>{record.updated_at}</td>
                        <td>{record.status}</td>
                </tr>
            )
        }

        return (
            <div>
                <button type="button" className="btn btn-outline-primary" onClick={onAddEntryButtonClick}>Add Entry</button>

                <div className="row justify-content-center">
                    <table className="table table-responsive">
                        <thead>
                            <tr>
                                <th scope="col">Sl No</th>
                                <th scope="col">Entry ID</th>
                                <th scope="col">Title</th>
                                <th scope="col">Created At</th>
                                <th scope="col">Updated At</th>
                                <th scope="col">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                data.records.map((listValue, index) => {
                                    return generateRow(listValue, index)
                                })
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        )

    }

    return renderTable()
}

export default CollectionDetails;
