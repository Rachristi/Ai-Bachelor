// apiHelper.ts
export class ApiHelper {
    static async sendQuestion(question: string, method: string, comments: { message: string; sender: string }[], auther: string): Promise<{ comments: { message: string; sender: string }[], error: string, isLoading: boolean, question: string }> {
        let answer: string = "";
        let error: string = "";
        let isLoading = true;
        try {
            const response = await fetch("http://localhost:5000/answer", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question, method }),
            });

            if (!response.ok) {
                answer = "Failed to fetch data";
                auther = "systemAlert";
                comments = [...comments, { message: answer, sender: auther }];
                throw new Error("Failed to fetch data");
            }

            const data = await response.json();
            answer = data.answer;
            auther = data.sender;
            comments = [...comments, { message: answer, sender: auther }];
            error = ""; // Clear any previous error
        } catch (err) {
            error = "An error occurred while fetching data";
            console.error(err);
        }

        question = "";
        isLoading = false;

        return { comments, error, isLoading, question };
    }

    static async createEmbeddings(): Promise<void> {
        const response = await fetch("http://localhost:5000/create-embeddings", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }
    }

}
