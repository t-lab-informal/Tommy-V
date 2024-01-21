`include "config.svh"

module register #(
    parameter B_WIDTH = 32,
) (
    input           write_en,
    input  [4:0]    rd_addr,
    input  [4:0]    rs1_addr,
    input  [4:0]    rs2_addr,
    input  [31:0]   rd_data,
    output [31:0]   rs1_data,
    output [31:0]   rs2_data
);

    logic [31:0][B_WIDTH-1:0] register;

    // assign register[0] = 'b0;

    initial begin
        // Zero register
        register[0] = 'b0;

        // First value of Register x2(sp) is `STACK_ADDRESS
        register[2] = `STACK_ADDRESS;
    end

    always_comb begin : data_read
        rs1_data <= register[rs1_addr];
        rs2_data <= register[rs2_addr];
    end

    always_ff begin : data_write
        if (write_en) begin
            if (rd_addr != 5'b0) register[rd_addr] <= rd_data;
        end
    end


endmodule
