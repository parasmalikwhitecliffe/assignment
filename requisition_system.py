# requisition_system.py
# Prototype of the requisition system (Assessment 2)


class Requisition:
    """Represents one requisition submitted by a staff member."""

    # Shared by all requisitions (not stored inside each object)
    next_id = 10001          # the next unique requisition ID
    APPROVAL_LIMIT = 500     # totals below this are approved automatically

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

        return self.total

    def approve_requisition(self):
        """
        Decide the status using the total:
        - Less than $500  -> Approved (reference number is created)
        - $500 or more    -> Pending (waits for a manager's response)
        """
        if self.total < Requisition.APPROVAL_LIMIT:
            self.status = "Approved"
            # Staff ID + last 3 digits of the requisition ID
            self.approval_reference = self.staff_id + str(self.requisition_id)[-3:]
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"