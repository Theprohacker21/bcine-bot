# Discord Support Bot

A Discord bot that provides a comprehensive support ticket system with dropdown menus, role-based permissions, and ticket management features.

## Features

- **Support Dropdown Menu**: Users can select between "General" or "Support/Bug/Suggestion" ticket types
- **Automatic Ticket Channels**: Creates dedicated channels for each ticket in the appropriate category
- **Claim/Unclaim System**: Support staff can claim tickets with the designated role
- **Claim Buttons**: 
  - Green "Claim" button when unclaimed
  - Gray "Unclaim" button when claimed (only the claimer can unclaim)
- **Close Tickets**: Support staff can close tickets with a confirmation dialog
- **Confirmation System**: Before closing, users must confirm via Yes/No buttons

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Copy `.env.example` to `.env`
   - Add your Discord bot token to the `.env` file

3. **Configure Bot**:
   - Replace the channel and role IDs in `cogs/support.py` with your actual IDs:
     - `1504781109681193001`: Support embed channel
     - `1504828516347412512`: General ticket category
     - `1505026545100525660`: Support/Bug category
     - `1465374880865456261`: Support staff role

4. **Run the Bot**:
   ```bash
   python main.py
   ```

## Commands

- `/support`: Posts the support system embed (Admin only)

## Channel IDs Configuration

Update these IDs in `cogs/support.py`:

- **Support Channel**: `1504781109681193001` - Where the support embed is posted
- **General Category**: `1504828516347412512` - Category for general tickets
- **Support/Bug Category**: `1505026545100525660` - Category for support/bug/suggestion tickets
- **Support Role**: `1465374880865456261` - Role required to claim and close tickets

## Ticket Workflow

1. User clicks the dropdown and selects a ticket type
2. A new channel is created in the appropriate category
3. Support staff claim the ticket using the "Claim" button
4. Button changes to "Unclaim" (gray) and only the claimer can unclaim
5. Support staff click "Close" to end the ticket
6. A confirmation dialog appears (Yes/No)
7. Clicking "Yes" deletes the channel; "No" dismisses the dialog and keeps the ticket open
