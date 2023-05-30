export const parseImport = (source, wdDelim, cardDelim) => {
	const cards = source.split(cardDelim);
	const results = [];
	for (const card of cards) {
		const word = card.split(wdDelim)[0];
		const defi = card.split(wdDelim)[1];
		results.push({ word, definition: defi });
	}
	return results;
};
export const parseExport = (source, wdDelim, cardDelim) => {
	let result = '';
	for (const card of source) {
		const col = card.word + wdDelim + card.definition;
		result += col + cardDelim;
	}
	// remove last card delim
	result = result.slice(0, -cardDelim.length);
	return result;
};

function main() {
	let sample_input = 'word1 def1\nword2 def2\nword3 def3';
	let result1 = parseImport(sample_input, ' ', '\n');
	console.log(result1);
	let result2 = parseExport(result1, ' ', '\n');
	console.log(result2);
}
