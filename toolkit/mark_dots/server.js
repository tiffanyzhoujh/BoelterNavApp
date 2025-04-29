const express = require('express');
const fs = require('fs');
const app = express();

app.use(express.json());
app.use(express.static('.'));

const floorname = "9f"; // TODO: CHANGE
const csvFile = floorname+'-new-coord.csv';

if (!fs.existsSync(csvFile)) {
    fs.writeFileSync(csvFile, 'Label,X,Y\n');
}

app.post('/log', (req, res) => {
    const { x, y, number, floorname} = req.body;
    const logEntry = `${floorname}-${number},${x},${y}\n`;

    fs.appendFile(csvFile, logEntry, err => {
        if (err) {
            console.error('Error writing to file:', err);
            res.status(500).send('Error logging data');
        } else {
            res.sendStatus(200);
        }
    });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
