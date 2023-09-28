import mongodb from 'mongodb';

export const getClient = () => {
    const client = mongodb.MongoClient(process.env.MONGO_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    });
    return client;
}

export const getDb = () => {
    const client = getClient();
    return client.db("at");
}

export const getCollection = (collection) => {
    const db = getDb();
    return db.collection(collection);
}

export const getStories = async () => {
    const stories = await getCollection("stories").find({}).toArray();
    return stories;
}

export const getGroups = async () => {
    const groups = await getCollection("groups").find({}).toArray();
    return groups;
}