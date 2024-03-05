import { React, useEffect, useState } from "react";

import { useNavigate, useParams } from "react-router-dom";

const CreateEntry = (props) => {
    const urlParams = useParams();

    const [collection, setCollection] = useState({});

    const [entryTitle, setEntryTitle] = useState("");
    const [entryContent, setEntryContent] = useState("");
    const [shouldPublish, setShouldPublish] = useState(false);

    useEffect(() => { getCollectionById() }, [])

    const navigate = useNavigate();

    async function handleFormSubmit(e) {
        // get the content of the form
        // getting the content of the form will have to be done based on the value of collection.template
        // since the form is going to be rendered in the same order as the template, I can just loop through the template
        // and get the values based on they
        // but this does mean that I'll have to set the name of the form element to the key value from the template
        const data = {
            collection_id: collection.collection_id,
            title: entryTitle,
            content: {
                content: entryContent,
            },
            publish: shouldPublish,
        }

        const userToken = JSON.parse(localStorage.getItem("user")).token;

        const response = await fetch(
            "http://localhost:8000/v1/journal/entries/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + userToken,
                },
                body: JSON.stringify(data),
            }
        )

        const entry = await response.json();

        if (!response.ok) {
            console.log(response);
            throw new Error(entry.detail);
        }

        navigate(`/collections/${collection.collection_id}/entries/${entry.entry_id}`);
    }

    async function getCollectionById() {
        // const userToken = JSON.parse(localStorage.getItem("user")).token;

        // const response = await fetch(
        //     "http://localhost:8000/v1/journal/collections/" + urlParams.collectionId,
        //     {
        //         method: "GET",
        //         headers: {
        //             Authorization: "Bearer " + userToken,
        //             "Content-Type": "application/json",
        //         },
        //     }
        // )
        // if (!response.ok) {
        //     console.log("error fetching data from server");
        //     throw new Error("error fetching data from server");
        // }

        // const data = await response.json();

        const data = {
            collection_id: urlParams.collectionId,
            name: "test_e59m",
            template: {
                fields: [
                    {
                        key: "title",
                        display_name: "Title",
                    },
                    {
                        key: "content",
                        display_name: "Content",
                    },
                ]
            },
            active: true,
            created_at: "2023-12-02T18:10:33Z",
        }

        setCollection(data)
    }

    const handlePublishCheck = (e) => {
        setShouldPublish(e.target.checked);
    }

    const renderForm = () => {
        // loop through collection.template
        // call the appropriate formIO class to build the form
        // when building the form, set the name to the value of key
        // once the form has been built, add the submit button to the end of the component
        // the behavior of handleSubmit can be as it already is
        return (
        <div>
            <h1>{collection.name}</h1>
            <form id="collectionEntry">
                <div className="form-group">
                    <label htmlFor="collectionEntry">Title</label>
                    <input className="form-control" htmlFor="collectionEntry" placeholder="Enter title" value={entryTitle} onChange={(e) => {setEntryTitle(e.target.value)}}></input>
                </div>
                <div className="form-group">
                    <label htmlFor="collectionEntry">Content</label>
                    <textarea id="entry-content" name="textarea" value={entryContent} onChange={(e) => {setEntryContent(e.target.value)}} cols={100} rows={10} style={{width: "100%"}}/>
                </div>
                <div className="form-group form-check">
                    <input type="checkbox" htmlFor="collectionEntry" className="form-check-input" id="publish-entry-checkbox" value={shouldPublish} onChange={handlePublishCheck}></input>
                    <label className="form-check-label" htmlFor="publish-entry-checkbox">Publish this</label>
                </div>
                <button type="button" className="btn btn-primary" onClick={handleFormSubmit}>Save Entry</button>
            </form>
        </div>
        )
    }

    return renderForm()
}

export default CreateEntry;
