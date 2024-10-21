# Referee Delegation System

**System for delegating volleyball referees to matches**

## Project Overview

The Referee Delegation System is a web application designed to facilitate the delegation of referees to volleyball matches. 
The system aims to streamline the process of managing matches, referees, and teams across various seasons and competitions, 
while taking into account referees' licenses, availability, (location), and rating. It also provides an intuitive interface 
for managing delegations, sending notifications, and optionally, allowing referees to track their assignments.

## Objectives of the Project

The main objectives of the project are to:

- Manage matches, referees, and teams across seasons and competitions.
- Manually (or automatically in future extensions) delegate suitable referees to matches based on license, availability, (location), and rating.
- Allow referees to enter their availability and track their match assignments.
- Possibly send email (and/or SMS) notifications to referees about assigned matches.

### Database (`models`)
ER diagram:
![ER Diagram](/files/ER_diagram.png)

## System Description

### 1. User Roles

- **Competition Manager**: Manages competitions, matches, and teams.
- **Referee Manager**: Oversees referees, their licenses, and assignments.
- **Delegation Manager**: Manually delegates referees to matches.
- **Site Manager**: Has permissions of all the managers.
- **stuff**: "superuser" - has access to the Django Administration panel.
- **Referee**: Enters availability and tracks assigned matches.

### 2. Referee Management

Referees are categorized based on their licenses:

- **AM (International)**: Can referee all matches.
- **A (Extraleague)**: Can referee all but international matches.
- **B (Premier League)**: Can referee premier league and lower competitions.
- **C (Regional)**: Can referee only regional competitions.

Each referee has the following attributes:
- Name and contact information.
- Location (city).
- Rating (0-100 scale).
- Availability (date and time ranges).
- License (AM, A, B, C).

Referees can serve in the following roles:
- **1st referee (1.R)**, **2nd referee (2.R)**, **1st line judge (1.L)**, **2nd line judge (2.L)**.

### 3. Match Management

Every match has the following attributes:
- **Date and time** of the match.
- **Location** (city or hall).
- **Competition in season** (e.g., Extraleaugue men 2024/2025, 1st league women 2024/2025).
- **Level** of the match (extraleaugue, premier league, regional competitions).
- **Teams (home and away)**: Assigned teams from registered teams.
- **Delegated referees**: The system assigns referees based on their license, availability, location, and rating.

### 4. Team Management

Each team is defined by:
- **Team Name**
- **Location** (city)
- **Contact person** (name, phone, email)

### 5. Season and Competition Management

- **Season**: E.g., 2024/2025, 2023/2024, etc.
- **Competition**:
  - Extraleague: Extraleague men, Extraleague women...
  - First League: 1st league men, 1st league women, juniors...
  - Regional competitions: Cadets, Cadet girls, etc.

## Referee Delegation Process

### 1. Manual Delegation

- The Delegation Manager can manually assign referees based on their license, availability, (location), and rating.
- The system displays suitable referees.
- **Optional**: Integration with Google Maps API (or other map services) for calculating distances between referees and match locations.

### 2. Notifications

- **Optional**: Referees receive email (and sms) notifications about their assignments.
- **Optional**: SMS notifications via Twilio or other SMS services.

### 3. Automated Delegation (Future Extension)

- The system automatically assigns referees based on the following criteria:
  - **Availability**: Ensuring referees are available for the match date and time.
  - **License**: Ensuring the referee holds the necessary license for the match level.
  - **Rating**: Higher-rated referees are preferred for important matches.
  - **Location**: Referees closer to the match location are preferred.

## User Interface

### 1. For Administrators

- **Managers**: Add, edit, or delete operations on the assigned tasks based on their specialisation (competitions, referees, etc.)

### 2. For Referees

- **Enter Their Unavailability**: Referees can specify date and time ranges when they are unavailable.
- **Optional: View Assigned Matches**: Referees can view upcoming and past match assignments.

### Possible Extensions

- **Calendar Integration**: Referees can view their availability and match assignments on an interactive calendar (e.g., via FullCalendar.js).
- **Export to iCal**: Ability to export assignments and availability to a personal calendar.

## System Architecture

### 1. Back-end

- **Framework**: Django for managing matches, referees, and delegations.
- **Database Management**: Django ORM for CRUD operations.
- **Notifications**: Django Email (and possibly Twilio for SMS) integrations.
- **Optional - Automated Delegation**: An algorithm that factors in availability, license, rating, and location of referees.

### 2. Front-end

- **HTML/CSS and Django Templates**: For creating a user-friendly interface.
- **Interactive Calendars**: Implementation of interactive calendars for referees using JavaScript libraries like FullCalendar.js.

## Additional Features (Future Development)

- **Geolocation**: Integration of Google Maps API to visualize distances between referees and match locations.
- **Referee Performance Evaluation**: Allow coaches or team managers to evaluate referees after matches, impacting their rating.

## Project Structure

### 1. `accounts` app

#### 1.1. Database Structure

- **ProfileReferee**: Links to the User model and the Referee model.
- **ProfileManager**: Links to the User model and contains manager-specific fields.

#### 1.2. Functionality

- User profiles, referee profiles, and manager profiles management.

### 2. `referees` app

#### 2.1. Database Structure

- **Referee**: Contains name, surname, date of birth, city, license, rating, and contact details.
- **RefereeLicenceType**: Defines the licence types connected to the Competition_levels
- **Unavailability**: Defines periods when referees are unavailable.

#### 2.2. Functionality

- Manage referee details and unavailability.

### 3. `competitions` app

#### 3.1. Database Structure

- **City**: Contains city names.
- **Team**: Contains team names, city, and contact details.
- **CompetitionInSeason**: Links competitions to seasons.
- **Season**: Defines start and end dates.
- **Competition**: Defines competition name, season, level, and category.
- **Match**: Contains details of the match (code, competition, teams, date, location).

#### 3.2. Functionality

- Manage teams, competitions, and matches.

### 4. `delegations` app

#### 4.1. Database Structure

- **Delegation**: Links referees to matches and defines their role (e.g., 1st referee, line judge).
- **Referee Role**: Defines the referee roles in a match.


#### 4.2. Functionality

- Manage referee delegations.