const express = require('express');
const kue = require('kue');
const redis = require('redis');
const { promisify } = require('util');

const client = redis.createClient();
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

let numberOfAvailableSeats = 50;
let reservationEnabled = true;

async function reserveSeat(number) {
    await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
    const seats = await getAsync('available_seats');
    return seats ? parseInt(seats) : 0;
}

const queue = kue.createQueue();

const app = express();

app.get('/available_seats', (req, res) => {
    res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: "Reservation are blocked" });
    }
    queue.create('reserve_seat').save();
    res.json({ status: "Reservation in process" });
});

app.get('/process', async (req, res) => {
    res.json({ status: "Queue processing" });
    await processQueue();
});

async function processQueue() {
    const currentSeats = await getCurrentAvailableSeats();
    if (currentSeats === 0) {
        reservationEnabled = false;
    }
    if (currentSeats >= 0) {
        queue.process('reserve_seat', async (job, done) => {
            try {
                await reserveSeat(currentSeats - 1);
                console.log(`Seat reservation job ${job.id} completed`);
                done();
            } catch (error) {
                console.error(`Seat reservation job ${job.id} failed: ${error.message}`);
                done(error);
            }
        });
    } else {
        queue.process('reserve_seat', (job, done) => {
            const error = new Error('Not enough seats available');
            console.error(`Seat reservation job ${job.id} failed: ${error.message}`);
            done(error);
        });
    }
}
reserveSeat(numberOfAvailableSeats);

const PORT = 1245;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
