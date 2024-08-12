import { Lead } from "../hooks/FormHelpers";


export const PostLead = async (lead: Lead) => {
    try {
        const response = await fetch('http://localhost:5000/api/leads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(lead),
        });
        if (!response.ok) {
            throw new Error('Failed to post lead');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}
