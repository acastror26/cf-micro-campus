
// User Service URLs
const userServiceUrl = process.env.REACT_APP_USER_SERVICE_URL || '';
const generateTokenUrl = `${userServiceUrl}/token`;
const validateTokenUrl = `${userServiceUrl}/token/validate`;
const userServiceUsersUrl = `${userServiceUrl}/users`;

// Reservation Service URLs
const reservationServiceUrl = process.env.REACT_APP_RESERVATION_SERVICE_URL || '';
const reservationServiceRoomsUrl = `${reservationServiceUrl}/api/rooms/`;
const reservationServiceResourceTypesUrl = `${reservationServiceUrl}/api/resource-types/`;
const reservationServiceResourcesUrl = `${reservationServiceUrl}/api/resources/`;
const reservationServiceReservationsUrl = `${reservationServiceUrl}/api/reservations/`;
const reservationServiceReservationsUsersUrl = `${reservationServiceUrl}/api/users/`;

const config = {
    userServiceUrl: userServiceUrl,
    generateTokenUrl: generateTokenUrl,
    validateTokenUrl: validateTokenUrl,
    userServiceUsersUrl: userServiceUsersUrl,
    reservationServiceUrl: reservationServiceUrl,
    reservationServiceRoomsUrl: reservationServiceRoomsUrl,
    reservationServiceResourceTypesUrl: reservationServiceResourceTypesUrl,
    reservationServiceResourcesUrl: reservationServiceResourcesUrl,
    reservationServiceReservationsUrl: reservationServiceReservationsUrl,
    reservationServiceReservationsUsersUrl: reservationServiceReservationsUsersUrl
};

export default config;