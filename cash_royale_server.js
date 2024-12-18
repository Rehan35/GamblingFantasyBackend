import express from 'express';
import dotenv from 'dotenv';
import path from 'path';
import axios from 'axios';
import querystring from 'querystring'

dotenv.config({ path: path.resolve('./environment-variables', '.env') });

const app = express();
const port = 8080;

app.use(express.json());

let items = [
    { id: 1, name: "Item 1" },
    { id: 2, name: "Item 2" },
    { id: 3, name: "Item 3" }
];

// --- Routes ---

// 1. GET - Home route
app.get('/', (req, res) => {
    res.send('Welcome to My API!');
});

// 2. GET - Fetch all items
app.get('/api/items', (req, res) => {
    res.json(items);
});

app.post('/api/get_events', async (req, res) => {
    const parameters = {
        sport: req.body.sport,
        apiKey: process.env.ODDS_API_KEY
    }

    const events_query = `${process.env.ODDS_API_URL_HEADER}/v4/sports/${parameters.sport}/events?apiKey=${parameters.apiKey}`

    try {
        const response = await axios.get(events_query);
        console.log(response.data);
        res.json({success: true, data: response.data});
    } catch(error) {
        console.log(error);
        res.json({success: false});
    }
});

app.post('/api/get_event_odds', async (req, res) => {
    const parameters = {
        sport: req.body.sport,
        apiKey: process.env.ODDS_API_KEY,
        eventID: req.body.eventID,
        regions: req.body.regions,
        markets: req.body.markets,
        oddsFormat: req.body.oddsFormat,
        bookmakers: req.body.bookmakers
    }

    const events_query = `${process.env.ODDS_API_URL_HEADER}/v4/sports/${parameters.sport}/events/${parameters.eventID}/odds?apiKey=${parameters.apiKey}&regions=${parameters.regions}&markets=${ parameters.markets.join("%2C") }&oddsFormat=${parameters.oddsFormat}&bookmakers=${parameters.bookmakers}`;
    console.log(events_query);
    try {
        const response = await axios.get(events_query);
        console.log(response.data);
        res.json({success: true, data: response.data.bookmakers[0].markets});
    } catch(error) {
        console.log(error);
        res.json({success: false});
    }
});

app.listen(port, () => {
    console.log(`API is running at http://localhost:${port}`);
});

