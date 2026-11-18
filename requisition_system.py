# requisition_system.py
# Prototype of the requisition system (Assessment 2)


class Requisition:
    """Represents one requisition submitted by a staff member."""

    # Shared by all requisitions (not stored inside each object)
    next_id = 10001          # the next unique requisition ID
    APPROVAL_LIMIT = 500     # totals below this are approved automatically
    all_requisitions = []    # keeps every submitted requisition

    def __init__(self, date, staff_id, staff_name):
        """Set up the basic details of a requisition."""
        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name

        # Give this requisition a unique ID, then increase the counter
        self.requisition_id = Requisition.next_id
        Requisition.next_id += 1

        # Starting values (updated later by the methods below)
        self.items = []                              # list of (item name, cost)
        self.total = 0
        self.status = "Pending"
        self.approval_reference = "Not available"

    def add_requisition(self, items):
        """
        Add the requisition items and return the total cost.
        'items' is a list of (item name, cost), for example:
        [("Printer paper", 40), ("Stapler", 15.50)]
        """
        # Check that the list is not empty
        if len(items) == 0:
            print("Error: a requisition must have at least one item.")
            return 0

        total = 0
        for item_name, cost in items:
            # Check that each cost is a valid positive number
            if cost <= 0:
                print("Error: the cost of '" + item_name + "' must be greater than 0.")
                return 0
            total = total + cost

        self.items = items
        self.total = total

        # Decide the status straight away based on the total
        self.approve_requisition()

        # Save the requisition so it appears in the display and statistics
        if self not in Requisition.all_requisitions:
            Requisition.all_requisitions.append(self)

        return self.total

    def approve_requisition(self):
        """
        Decide the status using the total:
        - Less than $500  -> Approved (reference number is created)
        - $500 or more    -> Pending (waits for a manager's response)
        """
        if self.total < Requisition.APPROVAL_LIMIT:
            self.status = "Approved"
            self.create_reference()
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

    def create_reference(self):
        """Create the approval reference: Staff ID + last 3 digits of the requisition ID."""
        self.approval_reference = self.staff_id + str(self.requisition_id)[-3:]

    def respond_to_requisition(self, decision):
        """
        A manager responds to a pending requisition.
        'decision' must be "Approved" or "Not approved".
        """
        # Only pending requisitions can be responded to
        if self.status != "Pending":
            print("Requisition " + str(self.requisition_id) + " is already " + self.status + ".")
            return False

        if decision == "Approved":
            self.status = "Approved"
            self.create_reference()
        elif decision == "Not approved":
            self.status = "Not approved"
            self.approval_reference = "Not available"
        else:
            print("Error: decision must be 'Approved' or 'Not approved'.")
            return False

        return True

    def display_requisition(self):
        """Print the information of this one requisition."""
        print("Date: " + self.date)
        print("Requisition ID: " + str(self.requisition_id))
        print("Staff ID: " + self.staff_id)
        print("Staff Name: " + self.staff_name)
        print("Total: $" + str(self.total))
        print("Status: " + self.status)
        print("Approval Reference Number: " + self.approval_reference)
        print()

    @classmethod
    def display_requisitions(cls):
        """Print the information of all the requisitions."""
        if len(cls.all_requisitions) == 0:
            print("No requisitions to display.")
            return

        for requisition in cls.all_requisitions:
            requisition.display_requisition()

    @classmethod
    def requisition_statistics(cls):
        """Count and print the requisition statistics."""
        total_submitted = len(cls.all_requisitions)
        approved = 0
        pending = 0
        not_approved = 0

        for requisition in cls.all_requisitions:
            if requisition.status == "Approved":
                approved = approved + 1
            elif requisition.status == "Pending":
                pending = pending + 1
            elif requisition.status == "Not approved":
                not_approved = not_approved + 1

        print("Statistics:")
        print("Displaying the Requisition Statistics")
        print()
        print("The total number of requisitions submitted: " + str(total_submitted))
        print("The total number of approved requisitions: " + str(approved))
        print("The total number of pending requisitions: " + str(pending))
        print("The total number of not approved requisitions: " + str(not_approved))

        return total_submitted, approved, pending, not_approved


# Quick check (the full testing comes in the last commit)
if __name__ == "__main__":
    req1 = Requisition("03/04/2024", "FN19", "John Paul")
    req1.add_requisition([("Paper", 200), ("Pens", 250)])    # $450 -> Approved

    req2 = Requisition("05/04/2024", "FN20", "Tracy Brown")
    req2.add_requisition([("Laptop", 1000)])                 # $1000 -> Pending

    req2.respond_to_requisition("Not approved")              # manager responds

    Requisition.display_requisitions()
    Requisition.requisition_statistics()