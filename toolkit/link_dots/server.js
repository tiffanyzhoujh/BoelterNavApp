const express = require('express');
const fs = require('fs');
const csv = require('csv-parser');
const app = express();

app.use(express.json());
app.use(express.static('.')); 

const floorname = "1f"; // TODO: CHANGE
const coordsFile = floorname+'-uniform-coord.csv'; 
const edgesFile = floorname+'-edges.json';

// Load coordinates from coord.csv
app.get('/get-coords', (req, res) => {
    let dots = [];
    
    if (!fs.existsSync(coordsFile)) return res.json([]);

    fs.createReadStream(coordsFile)
        .pipe(csv())
        .on('data', (row) => {
            const parts = row.Label.split('-'); // Split by '-'
            const number = parts.length > 1 ? parseInt(parts[1]) : null; // Take the second part as number
            dots.push({
                number: number,
                x: parseInt(row.X),
                y: parseInt(row.Y)
            });
        })
        .on('end', () => {
            res.json(dots);
        });
});

// Get edges
app.get('/get-edges', (req, res) => {
    if (!fs.existsSync(edgesFile)) return res.json({});
    
    let edges = JSON.parse(fs.readFileSync(edgesFile, 'utf8'));
    res.json(edges);
});

// Add an edge
app.post('/add-edge', (req, res) => {
    const { dot1, dot2 } = req.body;

    let edges = {};
    if (fs.existsSync(edgesFile)) {
        edges = JSON.parse(fs.readFileSync(edgesFile, 'utf8'));
    }

    if (!edges[dot1]) edges[dot1] = [];
    if (!edges[dot2]) edges[dot2] = [];

    if (!edges[dot1].includes(dot2)) edges[dot1].push(dot2);
    if (!edges[dot2].includes(dot1)) edges[dot2].push(dot1);

    fs.writeFileSync(edgesFile, JSON.stringify(edges, null, 2));
    res.sendStatus(200);
});


// Remove an edge
app.post('/remove-edge', (req, res) => {
    const { dot1, dot2 } = req.body;

    if (!fs.existsSync(edgesFile)) return res.sendStatus(404);

    let edges = JSON.parse(fs.readFileSync(edgesFile, 'utf8'));

    if (edges[dot1]) edges[dot1] = edges[dot1].filter(n => n !== dot2);
    if (edges[dot2]) edges[dot2] = edges[dot2].filter(n => n !== dot1);

    fs.writeFileSync(edgesFile, JSON.stringify(edges, null, 2));
    res.sendStatus(200);
});

app.listen(3001, () => console.log('Server running on http://localhost:3001'));
