## Borrowed

Backend for an app that allows users to list items that they lent to someone and which they own, but also the ones which they borrowed.

# Usage

To register an object, user must first create it at `POST /objects`. He/She can also view list of object that they currently have (borrowed or owned and not lent) at `GET /objects`.

To make a note of a borrow, user has to call `POST /borrow`, mentioning which object they borrow, to whom, and when the object should be returned.

User can also return borrowed objects at `POST /borrows/return-borrowed-object`, the borrow object will now have 'returned' status. The object will be available for next borrows.
