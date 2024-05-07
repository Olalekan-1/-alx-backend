import kue from 'kue';
import createPushNotificationsJobs from './8-job';

describe('createPushNotificationsJobs', () => {
    let queue;

    beforeEach(() => {
        queue = kue.createQueue({ disableSearch: true });
        queue.testMode.enter();
    });

    afterEach(() => {
        queue.testMode.clear();
        queue.testMode.exit();
    });

    it('should display an error message if jobs is not an array', () => {
        expect(() => {
            createPushNotificationsJobs(null, queue);
        }).to.throw('Jobs is not an array');
    });

    it('should create two new jobs to the queue', () => {
        const jobs = [
            { phoneNumber: '1234567890', message: 'Test message 1' },
            { phoneNumber: '0987654321', message: 'Test message 2' }
        ];

        createPushNotificationsJobs(jobs, queue);

        const createdJobs = queue.testMode.jobs;
        expect(createdJobs).to.have.lengthOf(2);
        expect(createdJobs[0].type).to.equal('push_notification_code_3');
        expect(createdJobs[0].data).to.deep.equal(jobs[0]);
        expect(createdJobs[1].type).to.equal('push_notification_code_3');
        expect(createdJobs[1].data).to.deep.equal(jobs[1]);
    });
});
