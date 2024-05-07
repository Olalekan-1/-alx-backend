import redis from 'redis';

const client = redis.createClient();

function createHash() {
    client.hset('HolbertonSchools', 'Portland', '50', redis.print);
    client.hset('HolbertonSchools', 'Seattle', '80', redis.print);
    client.hset('HolbertonSchools', 'New York', '20', redis.print);
    client.hset('HolbertonSchools', 'Bogota', '20', redis.print);
    client.hset('HolbertonSchools', 'Cali', '40', redis.print);
    client.hset('HolbertonSchools', 'Paris', '2', redis.print);
}

function displayHash() {
    client.hgetall('HolbertonSchools', (err, hash) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log(hash);
    });
}

client.on('connect', () => {
    console.log('Redis client connected to the server');
    
    createHash();
    displayHash();
});

client.on('error', (error) => {
    console.error(`Redis client not connected to the server: ${error}`);
});
