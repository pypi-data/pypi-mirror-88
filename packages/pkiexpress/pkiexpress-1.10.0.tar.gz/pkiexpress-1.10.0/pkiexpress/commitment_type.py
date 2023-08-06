class CommitmentType(object):
    PROOF_OF_APPROVAL = 'proof-of-approval'
    PROOF_OF_CREATION = 'proof-of-creation'
    PROOF_OF_DELIVERY = 'proof-of-delivery'
    PROOF_OF_ORIGIN   = 'proof-of-origin'
    PROOF_OF_RECEIPT  = 'proof-of-receipt'
    PROOF_OF_SENDER   = 'proof-of-sender'


    def __init__(self):
        pass

__all__ = ['CommitmentType']
