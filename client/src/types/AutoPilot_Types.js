/**
 * Date type
 @typedef AutoPilot
 @type {Object}

 @property {boolean} AcceptApplications
 @property {boolean} Active
 @property {boolean} RejectApplications
 @property {boolean} SendCandidatesAppointments
 @property {number} AcceptanceScore
 @property {number} RejectionScore
 @property {number} CompanyID
 @property {number} ID
 @property {string} Description
 @property {string} Name
 @property {OpenTimeSlot[]} OpenTimeSlots
 */

/**
 * Date type
 @typedef OpenTimeSlot
 @type {Object}

 @property {boolean} Active
 @property {number} AutoPilotID
 @property {number} Day
 @property {number} Duration
 @property {number} ID
 @property {string} From
 @property {string} To
 */

