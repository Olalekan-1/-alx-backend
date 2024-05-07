import redis from 'redis';


const subscriber = redis.createClient();

function handleMessage(channel, message) {
    console.log(message);
    if (message === 'KILL_SERVER') {
        subscriber.unsubscribe('holberton school channel');
        subscriber.quit();
    }
}

subscriber.on('connect', () => {
    console.log('Redis client connected to the server');

    subscriber.subscribe('holberton school channel');
});
subscriber.on('error', (error) => {
    console.error(`Redis client not connected to the server: ${error}`);
});
subscriber.on('message', handleMessage);
