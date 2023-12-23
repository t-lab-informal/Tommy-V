module TRV32I_core #(
    parameter B_WIDTH = 32;
) (
    input                       clk, rst;
    output  [31:0]              pc, inst;
    output  [B_WIDTH-1:0]       mem_addr;
    output                      mem_read_en, mem_write_en;
    output  [(B_WIDTH/8)-1:0]   write_byte_en;
    inout   [B_WIDTH-1:0]       mem_data;
);

    //datapath

    //ctlpath


endmodule
