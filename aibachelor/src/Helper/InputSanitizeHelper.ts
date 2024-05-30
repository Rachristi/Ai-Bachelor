export function sanitizeInput(input: string): string {
	if (!input) {
		throw new Error("Input cannot be empty");
	}

	const sanitizedInput = input
    .replace(/['";]+/g, '')
    .replace(/\b(SELECT|INSERT|DELETE|UPDATE|DROP|CREATE|ALTER|EXEC|UNION|--)\b/gi, '');
    
	if (sanitizedInput.trim().length === 0) {
		throw new Error("Please do not misuse the input field. I have feelings too!");
	}

	return sanitizedInput.trim();
}
